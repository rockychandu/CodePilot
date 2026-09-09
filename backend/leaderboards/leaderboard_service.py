"""
Leaderboard Domain Service
Aggregates global, weekly, XP, and streak rankings.
"""

from typing import List, Dict, Any
from codepilot.db.connection import get_db_session
from codepilot.db.models import User, Profile
from backend.cache.lru_cache import cache

class LeaderboardService:
    @staticmethod
    def get_leaderboard(board_type: str = "GLOBAL", limit: int = 50) -> Dict[str, Any]:
        cache_key = f"leaderboard_{board_type.upper()}_{limit}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        with get_db_session() as db:
            query = db.query(Profile).join(User, Profile.user_id == User.id).filter(User.is_active == True)

            if board_type.upper() == "STREAK":
                query = query.order_by(Profile.streak_days.desc(), Profile.xp.desc())
            elif board_type.upper() == "RATING":
                query = query.order_by(Profile.contest_rating.desc(), Profile.xp.desc())
            elif board_type.upper() == "PROBLEMS":
                query = query.order_by(Profile.problems_solved.desc(), Profile.xp.desc())
            else:
                query = query.order_by(Profile.xp.desc(), Profile.problems_solved.desc())

            profiles = query.limit(limit).all()
            rankings = []
            for i, p in enumerate(profiles, 1):
                rankings.append({
                    "rank": i,
                    "userId": p.user_id,
                    "username": p.user.username if p.user else "User",
                    "displayName": p.display_name or (p.user.username if p.user else "User"),
                    "avatarUrl": p.avatar_url,
                    "xp": p.xp,
                    "level": p.level,
                    "rankTitle": p.rank_title,
                    "streakDays": p.streak_days,
                    "problemsSolved": p.problems_solved,
                    "contestRating": p.contest_rating
                })

            result = {
                "type": board_type.upper(),
                "rankings": rankings,
                "totalParticipants": len(rankings)
            }
            cache.set(cache_key, result, ttl_seconds=60)
            return result
