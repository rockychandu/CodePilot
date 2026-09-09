"""
Contest Platform Service
"""

from typing import Optional, List, Dict, Any, Tuple
from backend.repositories.contest_repository import ContestRepository
from backend.repositories.history_repository import HistoryRepository

class ContestService:
    @staticmethod
    def get_all_contests() -> List[Dict[str, Any]]:
        return ContestRepository.get_all()

    @staticmethod
    def get_contest_by_id(contest_id: int) -> Optional[Dict[str, Any]]:
        return ContestRepository.get_by_id(contest_id)

    @staticmethod
    def register_user(contest_id: int, user_id: int) -> Tuple[bool, str]:
        contest = ContestRepository.get_by_id(contest_id)
        if not contest:
            return False, "Contest not found."
        
        success = ContestRepository.register_participant(contest_id, user_id)
        if success:
            HistoryRepository.record_activity(
                user_id=user_id,
                activity_type="CONTEST",
                title=f"Registered for {contest['title']}",
                description=f"Starts at {contest['startTime']}",
                details={"contestId": contest_id}
            )
            return True, "Successfully registered for contest."
        return False, "Registration failed."

    @staticmethod
    def get_contest_leaderboard(contest_id: int) -> List[Dict[str, Any]]:
        return ContestRepository.get_leaderboard(contest_id)
