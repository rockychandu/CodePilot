"""
Authentication Domain Service
Implements registration, authentication, tokens, session management, and password lifecycle.
"""

from typing import Tuple, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from codepilot.db.connection import get_db_session
from codepilot.db.models import User, Profile, UserSession, PasswordReset
from backend.security.passwords import generate_salt, hash_password, verify_password, evaluate_password_strength
from backend.security.jwt_tokens import create_access_token, generate_refresh_token
from backend.repositories.audit_repository import AuditRepository
from backend.repositories.history_repository import HistoryRepository

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str, display_name: Optional[str] = None) -> Tuple[bool, Any]:
        """Register a new user with strong password checks and profile creation."""
        username = username.strip()
        email = email.strip().lower()

        if len(username) < 3:
            return False, "Username must be at least 3 characters long."
        if "@" not in email or "." not in email:
            return False, "Valid email address required."

        strength = evaluate_password_strength(password)
        if not strength["isAcceptable"]:
            return False, f"Password too weak: {', '.join(strength['feedback'])}"

        with get_db_session() as db:
            if db.query(User).filter(User.username.ilike(username)).first():
                return False, "Username is already taken."
            if db.query(User).filter(User.email.ilike(email)).first():
                return False, "Email address is already registered."

            salt = generate_salt()
            pwd_hash = hash_password(password, salt)

            user = User(
                username=username,
                email=email,
                password_hash=pwd_hash,
                salt=salt,
                role="USER",
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.flush()

            profile = Profile(
                user_id=user.id,
                display_name=display_name or username,
                xp=100,
                level=1,
                rank_title="Novice Developer",
                streak_days=1
            )
            db.add(profile)
            db.commit()

            # Create session tokens
            token = create_access_token(user.id, user.username, user.role)
            refresh_tok = generate_refresh_token()
            session_rec = UserSession(
                user_id=user.id,
                token=token,
                refresh_token=refresh_tok,
                expires_at=datetime.now(timezone.utc) + timedelta(days=30),
                is_revoked=False
            )
            db.add(session_rec)
            db.commit()

            AuditRepository.log_event(action="REGISTER", resource_type="USER", user_id=user.id, resource_id=str(user.id))
            HistoryRepository.record_activity(
                user_id=user.id,
                activity_type="ACCOUNT",
                title="Account Created",
                description="Welcome to CodePilot Enterprise Developer Platform!"
            )

            return True, {
                "token": token,
                "refreshToken": refresh_tok,
                "user": user.to_dict(include_private=True)
            }

    @staticmethod
    def authenticate_user(identifier: str, password: str, ip_address: Optional[str] = None, user_agent: Optional[str] = None) -> Tuple[bool, Any]:
        """Authenticate user by username or email and return JWT."""
        identifier = identifier.strip()
        with get_db_session() as db:
            user = db.query(User).filter(
                (User.username.ilike(identifier)) | (User.email.ilike(identifier))
            ).first()

            if not user or not user.is_active:
                return False, "Invalid username/email or password."

            if not verify_password(password, user.salt, user.password_hash):
                AuditRepository.log_event(action="LOGIN_FAILED", resource_type="USER", user_id=user.id, ip_address=ip_address, status="FAILED")
                return False, "Invalid username/email or password."

            token = create_access_token(user.id, user.username, user.role)
            refresh_tok = generate_refresh_token()

            session_rec = UserSession(
                user_id=user.id,
                token=token,
                refresh_token=refresh_tok,
                ip_address=ip_address,
                user_agent=user_agent,
                expires_at=datetime.now(timezone.utc) + timedelta(days=30),
                is_revoked=False
            )
            db.add(session_rec)
            db.commit()

            AuditRepository.log_event(action="LOGIN_SUCCESS", resource_type="USER", user_id=user.id, ip_address=ip_address)
            HistoryRepository.record_activity(
                user_id=user.id,
                activity_type="LOGIN",
                title="Signed In",
                description=f"Logged in from {ip_address or 'browser'}"
            )

            return True, {
                "token": token,
                "refreshToken": refresh_tok,
                "user": user.to_dict(include_private=True)
            }

    @staticmethod
    def refresh_access_token(refresh_token: str) -> Tuple[bool, Any]:
        with get_db_session() as db:
            session_rec = db.query(UserSession).filter(
                UserSession.refresh_token == refresh_token,
                UserSession.is_revoked == False
            ).first()

            if not session_rec:
                return False, "Invalid or expired refresh token."

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
        with get_db_session() as db:
            session_rec = db.query(UserSession).filter(UserSession.token == token).first()
            if session_rec:
                session_rec.is_revoked = True
                db.commit()
                return True
            return False

    @staticmethod
    def request_password_reset(email: str) -> Tuple[bool, str]:
        with get_db_session() as db:
            user = db.query(User).filter(User.email.ilike(email.strip())).first()
            if not user:
                return True, "If that email exists, password reset instructions have been dispatched."
            
            import secrets
            reset_tok = secrets.token_urlsafe(32)
            reset_rec = PasswordReset(
                user_id=user.id,
                reset_token=reset_tok,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=2),
                is_used=False
            )
            db.add(reset_rec)
            db.commit()
            return True, "If that email exists, password reset instructions have been dispatched."

    @staticmethod
    def reset_password(token: str, new_password: str) -> Tuple[bool, str]:
        strength = evaluate_password_strength(new_password)
        if not strength["isAcceptable"]:
            return False, f"Password too weak: {', '.join(strength['feedback'])}"

        with get_db_session() as db:
            reset_rec = db.query(PasswordReset).filter(
                PasswordReset.reset_token == token,
                PasswordReset.is_used == False
            ).first()

            if not reset_rec or reset_rec.expires_at < datetime.now(timezone.utc):
                return False, "Invalid or expired password reset token."

            user = db.query(User).filter(User.id == reset_rec.user_id).first()
            if not user:
                return False, "User not found."

            salt = generate_salt()
            user.salt = salt
            user.password_hash = hash_password(new_password, salt)
            reset_rec.is_used = True
            db.commit()
            return True, "Password reset successfully. You can now login with your new credentials."
