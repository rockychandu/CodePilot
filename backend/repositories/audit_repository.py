"""
Audit Log Repository
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import json
from codepilot.db.connection import get_db_session
from codepilot.db.models import AuditLog

class AuditRepository:
    @staticmethod
    def log_event(
        action: str,
        resource_type: str,
        user_id: Optional[int] = None,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        status: str = "SUCCESS",
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=str(resource_id) if resource_id else None,
                ip_address=ip_address,
                status=status,
                details_json=json.dumps(details or {}),
                created_at=datetime.now(timezone.utc)
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            return log.to_dict()

    @staticmethod
    def get_logs(page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        with get_db_session() as db:
            query = db.query(AuditLog)
            total = query.count()
            logs = query.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
            return {
                "total": total,
                "page": page,
                "pageSize": page_size,
                "logs": [l.to_dict() for l in logs]
            }
