"""
CodePilot Contest Service
Manages algorithmic contests, registration, live participant scores, and penalty calculations.
"""

from datetime import datetime, timezone
import json
from codepilot.db.connection import db_session
from codepilot.db.models import Contest, ContestParticipant, Problem, Submission, User


class ContestService:
    @staticmethod
    def get_all_contests() -> list[dict]:
        db = db_session()
        contests = db.query(Contest).order_by(Contest.start_time.desc()).all()
        return [c.to_dict() for c in contests]

    @staticmethod
    def get_contest_by_id(contest_id: int) -> dict | None:
        db = db_session()
        contest = db.query(Contest).filter_by(id=contest_id).first()
        if not contest:
            return None
        return contest.to_dict()

    @staticmethod
    def register_user(contest_id: int, user_id: int) -> tuple[bool, str]:
        db = db_session()
        contest = db.query(Contest).filter_by(id=contest_id).first()
        if not contest:
            return False, "Contest not found."

        existing = db.query(ContestParticipant).filter_by(contest_id=contest_id, user_id=user_id).first()
        if existing:
            return True, "Already registered for this contest."

        participant = ContestParticipant(
            contest_id=contest_id,
            user_id=user_id,
            score=0,
            penalty=0,
            rank=0
        )
        db.add(participant)
        db.commit()
        return True, "Successfully registered for contest."

    @staticmethod
    def get_contest_leaderboard(contest_id: int) -> list[dict]:
        db = db_session()
        participants = db.query(ContestParticipant).filter_by(contest_id=contest_id).all()

        # Recalculate ranks based on score (desc) and penalty (asc)
        sorted_participants = sorted(
            participants,
            key=lambda p: (-p.score, p.penalty)
        )

        results = []
        for rank, p in enumerate(sorted_participants, 1):
            p.rank = rank
            results.append({
                "rank": rank,
                "userId": p.user_id,
                "username": p.user.username if p.user else "Anonymous",
                "score": p.score,
                "penalty": p.penalty,
            })
        db.commit()
        return results
