"""
Contest & Leaderboard Repository
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import Contest, ContestParticipant

class ContestRepository:
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db_session() as db:
            contests = db.query(Contest).filter(Contest.is_published == True).order_by(Contest.start_time.asc()).all()
            return [c.to_dict() for c in contests]

    @staticmethod
    def get_by_id(contest_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            contest = db.query(Contest).filter(Contest.id == contest_id).first()
            if not contest:
                return None
            return contest.to_dict()

    @staticmethod
    def register_participant(contest_id: int, user_id: int) -> bool:
        with get_db_session() as db:
            existing = db.query(ContestParticipant).filter(
                ContestParticipant.contest_id == contest_id,
                ContestParticipant.user_id == user_id
            ).first()
            if existing:
                return True
            
            part = ContestParticipant(
                contest_id=contest_id,
                user_id=user_id,
                score=0,
                penalty=0,
                rank=0,
                registered_at=datetime.now(timezone.utc)
            )
            db.add(part)
            db.commit()
            return True

    @staticmethod
    def get_leaderboard(contest_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            participants = db.query(ContestParticipant).filter(
                ContestParticipant.contest_id == contest_id
            ).order_by(ContestParticipant.score.desc(), ContestParticipant.penalty.asc()).all()
            
            board = []
            for i, p in enumerate(participants, 1):
                entry = p.to_dict()
                entry["rank"] = i
                board.append(entry)
            return board
