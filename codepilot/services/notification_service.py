"""
CodePilot In-App Notification Service
Dispatches and manages user alerts, contest reminders, and achievement unlocks.
"""

from codepilot.db.connection import db_session
from codepilot.db.models import Notification, User


class NotificationService:
    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False) -> list[dict]:
        db = db_session()
        query = db.query(Notification).filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
        return [n.to_dict() for n in notifications]

    @staticmethod
    def send_notification(user_id: int, title: str, message: str, category: str = "SYSTEM", action_url: str = "") -> dict:
        db = db_session()
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            category=category,
            action_url=action_url,
            is_read=False
        )
        db.add(notif)
        db.commit()
        return notif.to_dict()

    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> bool:
        db = db_session()
        notif = db.query(Notification).filter_by(id=notification_id, user_id=user_id).first()
        if notif:
            notif.is_read = True
            db.commit()
            return True
        return False
