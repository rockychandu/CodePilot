"""
CodePilot Admin Service
Enterprise administration controls, user management, audit logging, and platform telemetry.
"""

from codepilot.db.connection import db_session
from codepilot.db.models import User, Submission, CodeExecution, AuditLog, Problem, Contest, AIReview


class AdminService:
    @staticmethod
    def get_system_telemetry() -> dict:
        """Fetch high-level platform statistics for admin dashboard."""
        db = db_session()
        total_users = db.query(User).count()
        total_problems = db.query(Problem).count()
        total_submissions = db.query(Submission).count()
        accepted_submissions = db.query(Submission).filter_by(status="Accepted").count()
        total_executions = db.query(CodeExecution).count()
        total_ai_reviews = db.query(AIReview).count()
        total_contests = db.query(Contest).count()

        acceptance_rate = (
            f"{(accepted_submissions / total_submissions * 100):.1f}%"
            if total_submissions > 0
            else "0.0%"
        )

        return {
            "totalUsers": total_users,
            "totalProblems": total_problems,
            "totalSubmissions": total_submissions,
            "acceptedSubmissions": accepted_submissions,
            "acceptanceRate": acceptance_rate,
            "totalExecutions": total_executions,
            "totalAIReviews": total_ai_reviews,
            "totalContests": total_contests,
        }

    @staticmethod
    def get_all_users(page: int = 1, page_size: int = 20) -> dict:
        db = db_session()
        total = db.query(User).count()
        users = db.query(User).order_by(User.id.asc()).offset((page - 1) * page_size).limit(page_size).all()
        return {
            "total": total,
            "page": page,
            "pageSize": page_size,
            "items": [u.to_dict(include_private=True) for u in users]
        }

    @staticmethod
    def set_user_role(target_user_id: int, new_role: str) -> bool:
        db = db_session()
        user = db.query(User).filter_by(id=target_user_id).first()
        if user and new_role in ["USER", "MODERATOR", "INSTRUCTOR", "ADMIN"]:
            user.role = new_role
            db.commit()
            return True
        return False
