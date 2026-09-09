"""
Notification Domain Service
"""

from typing import List, Dict, Any
from backend.repositories.notification_repository import NotificationRepository

class NotificationService:
    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        return NotificationRepository.get_user_notifications(user_id=user_id, unread_only=unread_only)

    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> bool:
        return NotificationRepository.mark_as_read(notification_id=notification_id, user_id=user_id)

    @staticmethod
    def notify(user_id: int, title: str, message: str, category: str = "SYSTEM", action_url: str = "") -> Dict[str, Any]:
        return NotificationRepository.create_notification(
            user_id=user_id,
            title=title,
            message=message,
            category=category,
            action_url=action_url
        )
