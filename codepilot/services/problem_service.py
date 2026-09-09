"""
CodePilot Problem Service
Provides access to problem catalogs, test cases, submission histories,
and difficulty/category filtering.
"""

from codepilot.db.connection import db_session
from codepilot.db.models import Problem, TestCase, Submission


class ProblemService:
    @staticmethod
    def get_all_problems(difficulty: str = None, category: str = None, search: str = None) -> list[dict]:
        db = db_session()
        query = db.query(Problem)
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        if category:
            query = query.filter_by(category=category)
        if search:
            query = query.filter(
                (Problem.title.ilike(f"%{search}%")) |
                (Problem.description.ilike(f"%{search}%"))
            )
        problems = query.order_by(Problem.id.asc()).all()
        return [p.to_dict(include_test_cases=False) for p in problems]

    @staticmethod
    def get_problem_by_id(problem_id: int, include_hidden_tests: bool = False) -> dict | None:
        db = db_session()
        problem = db.query(Problem).filter_by(id=problem_id).first()
        if not problem:
            return None
        return problem.to_dict(include_test_cases=True, include_hidden=include_hidden_tests)

    @staticmethod
    def get_problem_by_slug(slug: str, include_hidden_tests: bool = False) -> dict | None:
        db = db_session()
        problem = db.query(Problem).filter_by(slug=slug).first()
        if not problem:
            return None
        return problem.to_dict(include_test_cases=True, include_hidden=include_hidden_tests)

    @staticmethod
    def get_user_submissions(user_id: int, problem_id: int = None, page: int = 1, page_size: int = 20) -> dict:
        db = db_session()
        query = db.query(Submission).filter_by(user_id=user_id)
        if problem_id:
            query = query.filter_by(problem_id=problem_id)

        total = query.count()
        submissions = query.order_by(Submission.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

        return {
            "total": total,
            "page": page,
            "pageSize": page_size,
            "totalPages": (total + page_size - 1) // page_size if total > 0 else 1,
            "items": [s.to_dict() for s in submissions]
        }
