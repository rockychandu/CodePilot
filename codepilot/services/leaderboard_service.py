"""
CodePilot Leaderboard Service
Calculates real-time rankings across global XP, solved problems, contest ratings, and streaks.
"""

from codepilot.db.connection import db_session
from codepilot.db.models import User, Profile


class LeaderboardService:
    @staticmethod
    def get_leaderboard(board_type: str = "GLOBAL", limit: int = 50) -> list[dict]:
        db = db_session()
        query = db.query(Profile).join(User).filter(User.is_active == True)

        board_type = board_type.upper()
        if board_type == "XP":
            query = query.order_by(Profile.xp.desc())
        elif board_type == "PROBLEMS":
            query = query.order_by(Profile.problems_solved.desc())
        elif board_type == "STREAK":
            query = query.order_by(Profile.streak_days.desc())
        elif board_type == "RATING":
            query = query.order_by(Profile.contest_rating.desc())
        else:  # GLOBAL default
            query = query.order_by(Profile.xp.desc(), Profile.problems_solved.desc())

        profiles = query.limit(limit).all()

        rankings = []
        for idx, prof in enumerate(profiles, 1):
            rankings.append({
                "rank": idx,
                "userId": prof.user_id,
                "username": prof.user.username if prof.user else "Developer",
                "displayName": prof.display_name or (prof.user.username if prof.user else "User"),
                "avatarUrl": prof.avatar_url,
                "xp": prof.xp,
                "level": prof.level,
                "rankTitle": prof.rank_title,
                "problemsSolved": prof.problems_solved,
                "contestRating": prof.contest_rating,
                "streakDays": prof.streak_days,
                "primaryLanguage": prof.primary_language
            })

        return rankings
