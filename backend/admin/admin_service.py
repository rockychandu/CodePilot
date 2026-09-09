"""
System Administration Domain Service
"""

from typing import Dict, Any, List, Optional
from codepilot.db.connection import get_db_session
from codepilot.db.models import User
from backend.analytics.analytics_service import AnalyticsService
from backend.repositories.audit_repository import AuditRepository

class AdminService:
    @staticmethod
    def get_system_telemetry() -> Dict[str, Any]:
        return AnalyticsService.get_system_telemetry()

    @staticmethod
    def get_all_users(page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        with get_db_session() as db:
            query = db.query(User)
            total = query.count()
            users = query.order_by(User.id.asc()).offset((page - 1) * page_size).limit(page_size).all()
            return {
                "total": total,
                "page": page,
                "pageSize": page_size,
                "users": [u.to_dict(include_private=True) for u in users]
            }

    @staticmethod
    def set_user_role(target_user_id: int, new_role: str) -> bool:
        valid_roles = {"USER", "MODERATOR", "INSTRUCTOR", "ADMIN"}
        if new_role.upper() not in valid_roles:
            return False

        with get_db_session() as db:
            user = db.query(User).filter(User.id == target_user_id).first()
            if not user:
                return False
            user.role = new_role.upper()
            db.commit()

            AuditRepository.log_event(
                action="ROLE_CHANGE",
                resource_type="USER",
                resource_id=str(target_user_id),
                details={"newRole": new_role.upper()}
            )
            return True
