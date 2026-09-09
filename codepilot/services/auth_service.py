"""
CodePilot Authentication Service
Handles user registration, credential validation, JWT tokens, session lifecycle,
password reset requests, and email verification tokens.
"""

from datetime import datetime, timezone, timedelta
import re
import uuid
from codepilot.db.connection import db_session
from codepilot.db.models import User, Profile, UserSession, PasswordReset, EmailVerification, ActivityHistory
from codepilot.utils.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_token


class AuthService:
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Verify password meets enterprise security criteria."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"\d", password):
            return False, "Password must contain at least one digit."
        return True, "Password is strong."

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(email_regex, email))

    @staticmethod
    def validate_username(username: str) -> tuple[bool, str]:
        """Validate username format (3-32 chars, alphanumeric and underscore)."""
        if len(username) < 3 or len(username) > 32:
            return False, "Username must be between 3 and 32 characters."
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            return False, "Username may only contain letters, numbers, and underscores."
        return True, "Valid username."

    @classmethod
    def register_user(cls, username: str, email: str, password: str, display_name: str = None) -> tuple[bool, dict | str]:
        db = db_session()
        username = username.strip()
        email = email.strip().lower()

        # Validate inputs
        u_valid, u_msg = cls.validate_username(username)
        if not u_valid:
            return False, u_msg

        if not cls.validate_email(email):
            return False, "Invalid email address format."

        p_valid, p_msg = cls.validate_password_strength(password)
        if not p_valid:
            return False, p_msg

        # Check existing user
        if db.query(User).filter_by(username=username).first():
            return False, "Username is already taken."
        if db.query(User).filter_by(email=email).first():
            return False, "Email address is already registered."

        pw_hash, salt = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=pw_hash,
            salt=salt,
            role="USER",
            is_active=True,
            is_verified=False
        )
        db.add(new_user)
        db.flush()

        # Create Profile
        new_profile = Profile(
            user_id=new_user.id,
            display_name=display_name or username,
            bio="New CodePilot developer.",
            primary_language="Python",
            xp=100,
            level=1,
            rank_title="Novice Explorer",
            streak_days=1,
            problems_solved=0,
            contest_rating=1200
        )
        db.add(new_profile)

        # Log Activity
        activity = ActivityHistory(
            user_id=new_user.id,
            activity_type="ACCOUNT_CREATED",
            title="Account Created",
            description=f"Welcome to CodePilot, {username}!"
        )
        db.add(activity)

        # Generate tokens
        token = create_access_token(new_user.id, new_user.username, new_user.role)
        refresh_token = create_refresh_token(new_user.id)

        session_entry = UserSession(
            user_id=new_user.id,
            token=token,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30)
        )
        db.add(session_entry)
        db.commit()

        return True, {
            "token": token,
            "refreshToken": refresh_token,
            "user": new_user.to_dict(include_private=True)
        }

    @classmethod
    def authenticate_user(cls, login_identifier: str, password: str, ip_address: str = None, user_agent: str = None) -> tuple[bool, dict | str]:
        db = db_session()
        ident = login_identifier.strip()
        user = db.query(User).filter(
            (User.username == ident) | (User.email == ident.lower())
        ).first()

        if not user:
            return False, "Invalid username/email or password."

        if not user.is_active:
            return False, "This account is inactive. Please contact support."

        if not verify_password(password, user.password_hash, user.salt):
            return False, "Invalid username/email or password."

        # Create token & session
        token = create_access_token(user.id, user.username, user.role)
        refresh_token = create_refresh_token(user.id)

        session_entry = UserSession(
            user_id=user.id,
            token=token,
            refresh_token=refresh_token,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30)
        )
        db.add(session_entry)

        # Record login activity
        activity = ActivityHistory(
            user_id=user.id,
            activity_type="LOGIN",
            title="User Logged In",
            description=f"Authenticated from {ip_address or 'Local Client'}"
        )
        db.add(activity)
        db.commit()

        return True, {
            "token": token,
            "refreshToken": refresh_token,
            "user": user.to_dict(include_private=True)
        }

    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> tuple[bool, dict | str]:
        db = db_session()
        session_entry = db.query(UserSession).filter_by(refresh_token=refresh_token, is_revoked=False).first()
        if not session_entry:
            return False, "Invalid or expired refresh token."

        user = session_entry.user
        if not user or not user.is_active:
            return False, "User account is unavailable."

        new_token = create_access_token(user.id, user.username, user.role)
        session_entry.token = new_token
        db.commit()

        return True, {
            "token": new_token,
            "refreshToken": refresh_token
        }

    @classmethod
    def revoke_session(cls, token: str) -> bool:
        db = db_session()
        session_entry = db.query(UserSession).filter_by(token=token).first()
        if session_entry:
            session_entry.is_revoked = True
            db.commit()
            return True
        return False

    @classmethod
    def request_password_reset(cls, email: str) -> tuple[bool, str]:
        db = db_session()
        user = db.query(User).filter_by(email=email.strip().lower()).first()
        if not user:
            # Prevent email enumeration by returning success message
            return True, "If an account with that email exists, reset instructions have been generated."

        token = str(uuid.uuid4())
        reset_entry = PasswordReset(
            user_id=user.id,
            reset_token=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=2)
        )
        db.add(reset_entry)
        db.commit()
        return True, token

    @classmethod
    def reset_password(cls, token: str, new_password: str) -> tuple[bool, str]:
        db = db_session()
        reset_entry = db.query(PasswordReset).filter_by(reset_token=token, is_used=False).first()
        if not reset_entry:
            return False, "Invalid or expired reset token."

        now = datetime.now(timezone.utc)
        expires_at = reset_entry.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < now:
            return False, "Reset token has expired."

        valid_pw, msg = cls.validate_password_strength(new_password)
        if not valid_pw:
            return False, msg

        user = db.query(User).filter_by(id=reset_entry.user_id).first()
        if not user:
            return False, "Associated user not found."

        pw_hash, salt = hash_password(new_password)
        user.password_hash = pw_hash
        user.salt = salt
        reset_entry.is_used = True
        db.commit()

        return True, "Password has been successfully updated."
