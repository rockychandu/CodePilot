"""
User Management and Profile Domain Service
"""

from typing import Optional, List, Dict, Any, Tuple
from codepilot.db.connection import get_db_session
from codepilot.db.models import User, Profile, UserSkill, ActivityHistory
from backend.repositories.user_repository import UserRepository
from backend.repositories.history_repository import HistoryRepository

class UserService:
    @staticmethod
    def get_profile_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            return user.to_dict(include_private=True)

    @staticmethod
    def get_public_profile(username: str) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            user = db.query(User).filter(User.username.ilike(username)).first()
            if not user:
                return None
            return user.to_dict(include_private=False)

    @staticmethod
    def update_profile(user_id: int, updates: Dict[str, Any]) -> Tuple[bool, Any]:
        res = UserRepository.update_profile(user_id, updates)
        if not res:
            return False, "Profile not found."
        return True, res

    @staticmethod
    def get_user_activity_history(
        user_id: int,
        page: int = 1,
        page_size: int = 20,
        activity_type: Optional[str] = None,
        language: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        return HistoryRepository.get_user_history(
            user_id=user_id,
            page=page,
            page_size=page_size,
            activity_type=activity_type,
            language=language,
            status=status,
            search=search
        )

    @staticmethod
    def add_user_activity(
        user_id: int,
        activity_type: str,
        title: str,
        description: str = "",
        language: Optional[str] = None,
        status: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return HistoryRepository.record_activity(
            user_id=user_id,
            activity_type=activity_type,
            title=title,
            description=description,
            language=language,
            status=status,
            details=details
        )
