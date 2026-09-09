"""
Complete Enterprise Authentication Service
"""

import secrets
from typing import Tuple, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from codepilot.db.connection import get_db_session
from codepilot.db.models import (
    User, Profile, UserSession, PasswordReset, EmailVerification,
    UserSettings, UserSkill, ActivityHistory
)
from backend.auth.password import generate_salt, hash_password, verify_password, evaluate_password_strength
from backend.auth.tokens import create_access_token, generate_refresh_token
from backend.auth.validators import validate_username, validate_email, validate_password_match
from backend.auth.rate_limit import auth_rate_limiter
from backend.repositories.audit_repository import AuditRepository
from backend.repositories.history_repository import HistoryRepository

def _is_expired(dt: Optional[datetime]) -> bool:
    if dt is None:
        return True
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt < now

class AuthService:
    @staticmethod
    def register_user(
        username: str,
        email: str,
        password: str,
        confirm_password: Optional[str] = None,
        display_name: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[bool, Any]:
        """Register a new user account with complete relational bootstrap."""
        # 1. Validation
        valid_u, u_err = validate_username(username)
        if not valid_u:
            return False, u_err

        valid_e, e_err = validate_email(email)
        if not valid_e:
            return False, e_err

        if confirm_password is not None:
            valid_m, m_err = validate_password_match(password, confirm_password)
            if not valid_m:
                return False, m_err

        strength = evaluate_password_strength(password)
        if not strength["isAcceptable"]:
            return False, f"Password too weak: {', '.join(strength['feedback'])}"

        clean_user = username.strip()
        clean_email = email.strip().lower()

        with get_db_session() as db:
            # Uniqueness check
            if db.query(User).filter(User.username.ilike(clean_user)).first():
                return False, "Username is already taken."
            if db.query(User).filter(User.email.ilike(clean_email)).first():
                return False, "An account with this email address already exists."

            # Password Hashing
            salt = generate_salt()
            pwd_hash = hash_password(password, salt)

            now = datetime.now(timezone.utc)
            user = User(
                username=clean_user,
                email=clean_email,
                password_hash=pwd_hash,
                salt=salt,
                role="USER",
                is_active=True,
                is_verified=True,
                last_login_at=now,
                created_at=now
            )
            db.add(user)
            db.flush()

            # Profile creation
            profile = Profile(
                user_id=user.id,
                display_name=display_name.strip() if display_name else clean_user,
                avatar_url="frontend/assets/logo.svg",
                bio="CodePilot Developer",
                primary_language="Python",
                preferred_languages='["Python", "JavaScript"]',
                xp=100,
                level=1,
                rank_title="Novice Developer",
                streak_days=1,
                problems_solved=0,
                contest_rating=1200,
                courses_completed=0
            )
            db.add(profile)

            # User Settings creation
            settings = UserSettings(
                user_id=user.id,
                theme="dark",
                email_notifications=True,
                editor_font_size="14px",
                editor_tab_size=4,
                editor_keymap="standard"
            )
            db.add(settings)

            # Initial Skill Record
            skill = UserSkill(
                user_id=user.id,
                skill_slug="python-basics",
                current_level=1,
                xp=100
            )
            db.add(skill)

            # Initial Activity Record
            activity = ActivityHistory(
                user_id=user.id,
                activity_type="ACCOUNT",
                title="Account Created",
                description="Welcome to CodePilot Enterprise Developer Platform!",
                language="python",
                status="SUCCESS",
                created_at=now
            )
            db.add(activity)

            # Session token pair
            token = create_access_token(user.id, user.username, user.role)
            refresh_tok = generate_refresh_token()
            session_rec = UserSession(
                user_id=user.id,
                token=token,
                refresh_token=refresh_tok,
                ip_address=ip_address,
                expires_at=now + timedelta(days=30),
                is_revoked=False
            )
            db.add(session_rec)

            db.commit()

            # Audit logging
            AuditRepository.log_event(
                action="REGISTER",
                resource_type="USER",
                user_id=user.id,
                resource_id=str(user.id),
                ip_address=ip_address
            )

            return True, {
                "token": token,
                "refreshToken": refresh_tok,
                "user": user.to_dict(include_private=True)
            }

    @staticmethod
    def authenticate_user(
        identifier: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Tuple[bool, Any]:
        """Authenticate user against database credentials with rate limiting and lockout protection."""
        clean_id = (identifier or "").strip()
        if not clean_id or not password:
            return False, "Username/Email and password are required."

        # Anti-Brute-Force Lockout Check
        if auth_rate_limiter.is_locked(ip_address, clean_id):
            auth_rate_limiter.record_attempt(ip_address, clean_id, False, "ACCOUNT_LOCKED_RATE_LIMIT")
            return False, "Too many failed login attempts. Your account is temporarily locked. Please try again later."

        with get_db_session() as db:
            user = db.query(User).filter(
                (User.username.ilike(clean_id)) | (User.email.ilike(clean_id))
            ).first()

            if not user:
                auth_rate_limiter.record_attempt(ip_address, clean_id, False, "USER_NOT_FOUND")
                return False, "Invalid username or password."

            if not user.is_active:
                auth_rate_limiter.record_attempt(ip_address, clean_id, False, "INACTIVE_ACCOUNT")
                return False, "Your account has been deactivated. Please contact support."

            if not verify_password(password, user.salt, user.password_hash):
                auth_rate_limiter.record_attempt(ip_address, clean_id, False, "INVALID_PASSWORD")
                AuditRepository.log_event(
                    action="LOGIN_FAILURE",
                    resource_type="USER",
                    user_id=user.id,
                    ip_address=ip_address,
                    status="FAILED"
                )
                return False, "Invalid username or password."

            # Login Success
            auth_rate_limiter.record_attempt(ip_address, clean_id, True)
            now = datetime.now(timezone.utc)
            user.last_login_at = now

            token = create_access_token(user.id, user.username, user.role)
            refresh_tok = generate_refresh_token()

            session_rec = UserSession(
                user_id=user.id,
                token=token,
                refresh_token=refresh_tok,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=now + timedelta(days=30),
                is_revoked=False
            )
            db.add(session_rec)
            db.commit()

            AuditRepository.log_event(
                action="LOGIN_SUCCESS",
                resource_type="USER",
                user_id=user.id,
                ip_address=ip_address
            )

            HistoryRepository.record_activity(
                user_id=user.id,
                activity_type="LOGIN",
                title="Signed In",
                description=f"Authenticated from {ip_address or 'browser'}"
            )

            return True, {
                "token": token,
                "refreshToken": refresh_tok,
                "user": user.to_dict(include_private=True)
            }

    @staticmethod
    def get_me(user_id: int) -> Optional[Dict[str, Any]]:
        """Fetch current authenticated user profile and settings."""
        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                return None
            return user.to_dict(include_private=True)

    @staticmethod
    def refresh_access_token(refresh_token: str) -> Tuple[bool, Any]:
        """Validate refresh token and issue fresh JWT access token."""
        if not refresh_token:
            return False, "Refresh token is required."

        with get_db_session() as db:
            session_rec = db.query(UserSession).filter(
                UserSession.refresh_token == refresh_token,
                UserSession.is_revoked == False
            ).first()

            if not session_rec or _is_expired(session_rec.expires_at):
                return False, "Invalid or expired session. Please sign in again."

            user = db.query(User).filter(User.id == session_rec.user_id).first()
            if not user or not user.is_active:
                return False, "User account is inactive."

            new_token = create_access_token(user.id, user.username, user.role)
            session_rec.token = new_token
            db.commit()

            return True, {
                "token": new_token,
                "refreshToken": refresh_token,
                "user": user.to_dict(include_private=True)
            }

    @staticmethod
    def revoke_session(token: str) -> bool:
        """Revoke current active token."""
        with get_db_session() as db:
            session_rec = db.query(UserSession).filter(UserSession.token == token).first()
            if session_rec:
                session_rec.is_revoked = True
                db.commit()
                return True
            return False

    @staticmethod
    def revoke_all_sessions(user_id: int) -> int:
        """Revoke all sessions for a user (Logout Other Sessions)."""
        with get_db_session() as db:
            count = db.query(UserSession).filter(
                UserSession.user_id == user_id,
                UserSession.is_revoked == False
            ).update({"is_revoked": True})
            db.commit()
            return count

    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str) -> Tuple[bool, str]:
        """Change user password after verifying current password."""
        strength = evaluate_password_strength(new_password)
        if not strength["isAcceptable"]:
            return False, f"New password too weak: {', '.join(strength['feedback'])}"

        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found."

            if not verify_password(current_password, user.salt, user.password_hash):
                return False, "Incorrect current password."

            new_salt = generate_salt()
            user.salt = new_salt
            user.password_hash = hash_password(new_password, new_salt)
            user.updated_at = datetime.now(timezone.utc)
            db.commit()

            AuditRepository.log_event(
                action="PASSWORD_CHANGE",
                resource_type="USER",
                user_id=user.id,
                resource_id=str(user.id)
            )

            return True, "Password updated successfully."

    @staticmethod
    def request_password_reset(email: str) -> Tuple[bool, str]:
        """Initiate password reset without account enumeration leakage."""
        clean_email = email.strip().lower()
        with get_db_session() as db:
            user = db.query(User).filter(User.email.ilike(clean_email)).first()
            if not user:
                return True, "If that email exists in our system, password reset instructions have been sent."

            reset_tok = secrets.token_urlsafe(32)
            reset_rec = PasswordReset(
                user_id=user.id,
                reset_token=reset_tok,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=2),
                is_used=False
            )
            db.add(reset_rec)
            db.commit()

            AuditRepository.log_event(
                action="PASSWORD_RESET_REQUEST",
                resource_type="USER",
                user_id=user.id
            )

            return True, "If that email exists in our system, password reset instructions have been sent."

    @staticmethod
    def reset_password(token: str, new_password: str) -> Tuple[bool, str]:
        """Reset password using reset token."""
        strength = evaluate_password_strength(new_password)
        if not strength["isAcceptable"]:
            return False, f"Password too weak: {', '.join(strength['feedback'])}"

        with get_db_session() as db:
            reset_rec = db.query(PasswordReset).filter(
                PasswordReset.reset_token == token,
                PasswordReset.is_used == False
            ).first()

            if not reset_rec or _is_expired(reset_rec.expires_at):
                return False, "Invalid or expired password reset token."

            user = db.query(User).filter(User.id == reset_rec.user_id).first()
            if not user:
                return False, "User account not found."

            new_salt = generate_salt()
            user.salt = new_salt
            user.password_hash = hash_password(new_password, new_salt)
            reset_rec.is_used = True
            db.commit()

            AuditRepository.log_event(
                action="PASSWORD_RESET",
                resource_type="USER",
                user_id=user.id
            )

            return True, "Your password has been successfully reset. You can now sign in."

    @staticmethod
    def verify_email(token: str) -> Tuple[bool, str]:
        """Verify email using verification token."""
        with get_db_session() as db:
            ver_rec = db.query(EmailVerification).filter(
                EmailVerification.verification_token == token,
                EmailVerification.is_used == False
            ).first()

            if not ver_rec or _is_expired(ver_rec.expires_at):
                return False, "Invalid or expired verification token."

            user = db.query(User).filter(User.id == ver_rec.user_id).first()
            if user:
                user.is_verified = True
                ver_rec.is_used = True
                db.commit()
                AuditRepository.log_event(action="EMAIL_VERIFIED", resource_type="USER", user_id=user.id)
                return True, "Email verified successfully."

            return False, "User not found."

    @staticmethod
    def resend_verification(email: str) -> Tuple[bool, str]:
        clean_email = email.strip().lower()
        with get_db_session() as db:
            user = db.query(User).filter(User.email.ilike(clean_email)).first()
            if not user:
                return True, "Verification email dispatched if account exists."

            ver_tok = secrets.token_urlsafe(32)
            ver_rec = EmailVerification(
                user_id=user.id,
                verification_token=ver_tok,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
                is_used=False
            )
            db.add(ver_rec)
            db.commit()
            return True, "Verification email dispatched."
