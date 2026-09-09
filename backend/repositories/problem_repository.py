"""
Problem Repository
Handles problem catalog, test cases, queries, filtering, and difficulty metrics.
"""

from typing import Optional, List, Dict, Any
from codepilot.db.connection import get_db_session
from codepilot.db.models import Problem, TestCase

class ProblemRepository:
    @staticmethod
    def get_all(difficulty: Optional[str] = None, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(Problem)
            if difficulty and difficulty.lower() != "all":
                query = query.filter(Problem.difficulty.ilike(difficulty))
            if category and category.lower() != "all":
                query = query.filter(Problem.category.ilike(category))
            if search:
                query = query.filter(
                    (Problem.title.ilike(f"%{search}%")) |
                    (Problem.description.ilike(f"%{search}%"))
                )
            
            problems = query.order_index if hasattr(query, 'order_index') else query.all()
            return [p.to_dict() for p in problems]

    @staticmethod
    def get_by_id(problem_id: int, include_test_cases: bool = False, include_hidden: bool = False) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            problem = db.query(Problem).filter(Problem.id == problem_id).first()
            if not problem:
                return None
            return problem.to_dict(include_test_cases=include_test_cases, include_hidden=include_hidden)

    @staticmethod
    def get_by_slug(slug: str, include_test_cases: bool = False) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            problem = db.query(Problem).filter(Problem.slug == slug).first()
            if not problem:
                return None
            return problem.to_dict(include_test_cases=include_test_cases)

    @staticmethod
    def get_test_cases_for_judge(problem_id: int) -> List[TestCase]:
        with get_db_session() as db:
            return db.query(TestCase).filter(TestCase.problem_id == problem_id).order_by(TestCase.order_index).all()
