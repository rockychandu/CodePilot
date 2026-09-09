"""
Submission Repository
Manages recording, retrieval, and statistics for competitive code submissions.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import Submission, Problem

class SubmissionRepository:
    @staticmethod
    def create_submission(
        user_id: int,
        problem_id: int,
        language: str,
        source_code: str,
        status: str,
        passed_tests: int,
        total_tests: int,
        runtime_seconds: float,
        memory_mb: float,
        compiler_output: str = "",
        test_results_json: str = "[]",
        contest_id: Optional[int] = None
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            sub = Submission(
                user_id=user_id,
                problem_id=problem_id,
                contest_id=contest_id,
                language=language,
                source_code=source_code,
                status=status,
                passed_tests=passed_tests,
                total_tests=total_tests,
                runtime_seconds=runtime_seconds,
                memory_mb=memory_mb,
                compiler_output=compiler_output,
                test_results_json=test_results_json,
                created_at=datetime.now(timezone.utc)
            )
            db.add(sub)
            
            # Update problem total/accepted count
            prob = db.query(Problem).filter(Problem.id == problem_id).first()
            if prob:
                prob.total_submissions += 1
                if status == "Accepted":
                    prob.accepted_submissions += 1

            db.commit()
            db.refresh(sub)
            return sub.to_dict()

    @staticmethod
    def get_user_submissions(user_id: int, problem_id: Optional[int] = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        with get_db_session() as db:
            query = db.query(Submission).filter(Submission.user_id == user_id)
            if problem_id:
                query = query.filter(Submission.problem_id == problem_id)
            
            total = query.count()
            submissions = query.order_by(Submission.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
            
            return {
                "total": total,
                "page": page,
                "pageSize": page_size,
                "submissions": [s.to_dict() for s in submissions]
            }
