"""
Activity History Repository
Persists timeline events for executions, problem submissions, contest participation, AI reviews, and learning progress.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import json
from codepilot.db.connection import get_db_session
from codepilot.db.models import ActivityHistory

class HistoryRepository:
    @staticmethod
    def record_activity(
        user_id: int,
        activity_type: str,
        title: str,
        description: str = "",
        language: Optional[str] = None,
        status: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            act = ActivityHistory(
                user_id=user_id,
                activity_type=activity_type,
                title=title,
                description=description,
                language=language,
                status=status,
                details_json=json.dumps(details or {}),
                created_at=datetime.now(timezone.utc)
            )
            db.add(act)
            db.commit()
            db.refresh(act)
            return act.to_dict()

    @staticmethod
    def get_user_history(
        user_id: int,
        page: int = 1,
        page_size: int = 20,
        activity_type: Optional[str] = None,
        language: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            query = db.query(ActivityHistory).filter(ActivityHistory.user_id == user_id)
            
            if activity_type and activity_type.upper() != "ALL":
                query = query.filter(ActivityHistory.activity_type == activity_type.upper())
            if language and language.lower() != "all":
                query = query.filter(ActivityHistory.language.ilike(language))
            if status and status.upper() != "ALL":
                query = query.filter(ActivityHistory.status.ilike(f"%{status}%"))
            if search:
                query = query.filter(
                    (ActivityHistory.title.ilike(f"%{search}%")) |
                    (ActivityHistory.description.ilike(f"%{search}%"))
                )

            total = query.count()
            activities = query.order_by(ActivityHistory.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
            formatted = [a.to_dict() for a in activities]

            return {
                "total": total,
                "page": page,
                "pageSize": page_size,
                "items": formatted,
                "activities": formatted
            }

    @staticmethod
    def get_activity_by_id(activity_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            act = db.query(ActivityHistory).filter(
                ActivityHistory.id == activity_id,
                ActivityHistory.user_id == user_id
            ).first()
            if not act:
                return None
            return act.to_dict()
