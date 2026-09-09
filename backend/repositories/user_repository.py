"""
User & Profile Repository
Handles data access for users, credentials, profiles, sessions, and skills.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import User, Profile, UserSession, UserSkill

class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        with get_db_session() as db:
            return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        with get_db_session() as db:
            return db.query(User).filter(User.username.ilike(username)).first()

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        with get_db_session() as db:
            return db.query(User).filter(User.email.ilike(email)).first()

    @staticmethod
    def create_user(username: str, email: str, password_hash: str, salt: str, role: str = "USER") -> User:
        with get_db_session() as db:
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                salt=salt,
                role=role,
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.flush()

            profile = Profile(
                user_id=user.id,
                display_name=username,
                xp=100,
                level=1,
                rank_title="Novice Developer",
                streak_days=1
            )
            db.add(profile)
            db.commit()
            db.refresh(user)
            return user

    @staticmethod
    def update_profile(user_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            profile = db.query(Profile).filter(Profile.user_id == user_id).first()
            if not profile:
                return None
            
            if "displayName" in updates:
                profile.display_name = updates["displayName"]
            if "bio" in updates:
                profile.bio = updates["bio"]
            if "primaryLanguage" in updates:
                profile.primary_language = updates["primaryLanguage"]
            if "preferredLanguages" in updates:
                import json
                profile.preferred_languages = json.dumps(updates["preferredLanguages"])
            if "avatarUrl" in updates:
                profile.avatar_url = updates["avatarUrl"]

            profile.updated_at = datetime.now(timezone.utc)
            db.commit()
            return profile.to_dict()

    @staticmethod
    def update_stats(user_id: int, xp_gain: int = 0, problems_solved_gain: int = 0) -> None:
        with get_db_session() as db:
            profile = db.query(Profile).filter(Profile.user_id == user_id).first()
            if profile:
                profile.xp += xp_gain
                profile.problems_solved += problems_solved_gain
                profile.level = max(1, 1 + (profile.xp // 250))
                db.commit()
