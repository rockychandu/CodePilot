"""
Background Maintenance & Cleanup Tasks
Cleans expired sessions, prunes temporary execution artifacts, and updates user streaks.
"""

from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import UserSession, PasswordReset

class MaintenanceTasks:
    @staticmethod
    def cleanup_expired_sessions() -> int:
        with get_db_session() as db:
            now = datetime.now(timezone.utc)
            deleted = db.query(UserSession).filter(UserSession.expires_at < now).delete()
            db.query(PasswordReset).filter(PasswordReset.expires_at < now).delete()
            db.commit()
            return deleted
