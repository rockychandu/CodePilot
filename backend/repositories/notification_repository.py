"""
Notification Repository
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import Notification

class NotificationRepository:
    @staticmethod
    def create_notification(user_id: int, title: str, message: str, category: str = "SYSTEM", action_url: str = "") -> Dict[str, Any]:
        with get_db_session() as db:
            notif = Notification(
                user_id=user_id,
                title=title,
                message=message,
                category=category,
                action_url=action_url,
                is_read=False,
                created_at=datetime.now(timezone.utc)
            )
            db.add(notif)
            db.commit()
            db.refresh(notif)
            return notif.to_dict()

    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(Notification).filter(Notification.user_id == user_id)
            if unread_only:
                query = query.filter(Notification.is_read == False)
            notifs = query.order_by(Notification.created_at.desc()).limit(50).all()
            return [n.to_dict() for n in notifs]

    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> bool:
        with get_db_session() as db:
            notif = db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()
            if not notif:
                return False
            notif.is_read = True
            db.commit()
            return True
