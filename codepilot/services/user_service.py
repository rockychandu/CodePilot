"""
CodePilot User & Profile Management Service
Manages user profiles, isolated activity history, XP leveling, and achievements.
"""

from datetime import datetime, timezone
import json
from codepilot.db.connection import db_session
from codepilot.db.models import User, Profile, ActivityHistory, UserSkill, Skill


class UserService:
    @staticmethod
    def get_profile_by_id(user_id: int) -> dict | None:
        db = db_session()
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return None
        return user.to_dict(include_private=True)

    @staticmethod
    def get_public_profile(username: str) -> dict | None:
        db = db_session()
        user = db.query(User).filter_by(username=username).first()
        if not user:
            return None
        return user.to_dict(include_private=False)

    @staticmethod
    def update_profile(user_id: int, updates: dict) -> tuple[bool, dict | str]:
        db = db_session()
        user = db.query(User).filter_by(id=user_id).first()
        if not user or not user.profile:
            return False, "User profile not found."

        profile = user.profile
        if "displayName" in updates:
            profile.display_name = updates["displayName"]
        if "bio" in updates:
            profile.bio = updates["bio"]
        if "primaryLanguage" in updates:
            profile.primary_language = updates["primaryLanguage"]
        if "preferredLanguages" in updates:
            langs = updates["preferredLanguages"]
            profile.preferred_languages = json.dumps(langs if isinstance(langs, list) else [langs])
        if "avatarUrl" in updates:
            profile.avatar_url = updates["avatarUrl"]

        db.commit()
        return True, user.to_dict(include_private=True)

    @staticmethod
    def add_user_activity(user_id: int, activity_type: str, title: str, description: str = None, language: str = None, status: str = None, details: dict = None) -> ActivityHistory:
        """Record an activity event isolated to the given user."""
        db = db_session()
        activity = ActivityHistory(
            user_id=user_id,
            activity_type=activity_type,
            title=title,
            description=description,
            language=language,
            status=status,
            details_json=json.dumps(details or {})
        )
        db.add(activity)
        db.commit()
        return activity

    @staticmethod
    def get_user_activity_history(user_id: int, page: int = 1, page_size: int = 20, activity_type: str = None, language: str = None, status: str = None, search: str = None) -> dict:
        """Fetch paginated, filtered activity history for a specific isolated user."""
        db = db_session()
        query = db.query(ActivityHistory).filter_by(user_id=user_id)

        if activity_type:
            query = query.filter_by(activity_type=activity_type)
        if language:
            query = query.filter_by(language=language)
        if status:
            query = query.filter_by(status=status)
        if search:
            query = query.filter(
                (ActivityHistory.title.ilike(f"%{search}%")) |
                (ActivityHistory.description.ilike(f"%{search}%"))
            )

        total = query.count()
        items = query.order_by(ActivityHistory.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "pageSize": page_size,
            "totalPages": (total + page_size - 1) // page_size if total > 0 else 1,
            "items": [item.to_dict() for item in items]
        }

    @staticmethod
    def award_xp(user_id: int, xp_amount: int) -> dict:
        """Add XP to user profile and calculate level progression."""
        db = db_session()
        user = db.query(User).filter_by(id=user_id).first()
        if not user or not user.profile:
            return {}

        profile = user.profile
        profile.xp += xp_amount
        # Level formula: level = floor(sqrt(xp / 100)) + 1
        new_level = int((profile.xp / 100) ** 0.5) + 1
        if new_level > profile.level:
            profile.level = new_level
            # Update rank title
            if new_level >= 30:
                profile.rank_title = "Grandmaster Engineer"
            elif new_level >= 20:
                profile.rank_title = "Principal Algorithmist"
            elif new_level >= 10:
                profile.rank_title = "Senior Coder"
            elif new_level >= 5:
                profile.rank_title = "Journeyman Developer"

        db.commit()
        return profile.to_dict()
