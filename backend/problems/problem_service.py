"""
Problem Catalog & Management Service
"""

from typing import Optional, List, Dict, Any
from backend.repositories.problem_repository import ProblemRepository

class ProblemService:
    @staticmethod
    def get_all_problems(difficulty: Optional[str] = None, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        return ProblemRepository.get_all(difficulty=difficulty, category=category, search=search)

    @staticmethod
    def get_problem_by_id(problem_id: int, include_test_cases: bool = True) -> Optional[Dict[str, Any]]:
        return ProblemRepository.get_by_id(problem_id=problem_id, include_test_cases=include_test_cases)

    @staticmethod
    def get_problem_by_slug(slug: str, include_test_cases: bool = True) -> Optional[Dict[str, Any]]:
        return ProblemRepository.get_by_slug(slug=slug, include_test_cases=include_test_cases)
