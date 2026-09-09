"""
History Domain Service
"""

from typing import Optional, Dict, Any
from backend.repositories.history_repository import HistoryRepository

class HistoryService:
    @staticmethod
    def get_history(
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
    def get_activity_detail(activity_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        return HistoryRepository.get_activity_by_id(activity_id=activity_id, user_id=user_id)
