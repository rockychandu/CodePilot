"""
Audit Logging Service
"""

from typing import Dict, Any, Optional
from backend.repositories.audit_repository import AuditRepository

class AuditService:
    @staticmethod
    def log(action: str, resource_type: str, user_id: Optional[int] = None, resource_id: Optional[str] = None, ip_address: Optional[str] = None, status: str = "SUCCESS", details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return AuditRepository.log_event(
            action=action,
            resource_type=resource_type,
            user_id=user_id,
            resource_id=resource_id,
            ip_address=ip_address,
            status=status,
            details=details
        )

    @staticmethod
    def get_audit_trail(page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        return AuditRepository.get_logs(page=page, page_size=page_size)
