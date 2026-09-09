"""
Unit Tests for Data Access Repositories
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.repositories.user_repository import UserRepository
from backend.repositories.problem_repository import ProblemRepository
from backend.repositories.contest_repository import ContestRepository
from backend.repositories.course_repository import CourseRepository
from backend.repositories.project_repository import ProjectRepository
from backend.repositories.history_repository import HistoryRepository

class TestRepositories(unittest.TestCase):
    def test_problem_repository_query(self):
        problems = ProblemRepository.get_all()
        self.assertIsInstance(problems, list)
        self.assertTrue(len(problems) > 0)
        p = ProblemRepository.get_by_id(problems[0]["id"])
        self.assertIsNotNone(p)

    def test_contest_repository(self):
        contests = ContestRepository.get_all()
        self.assertIsInstance(contests, list)

    def test_course_repository(self):
        courses = CourseRepository.get_all()
        self.assertIsInstance(courses, list)

    def test_history_repository(self):
        act = HistoryRepository.record_activity(
            user_id=1,
            activity_type="TEST",
            title="Automated Test Activity",
            description="Testing activity persistence",
            status="SUCCESS"
        )
        self.assertIsNotNone(act)
        self.assertEqual(act["title"], "Automated Test Activity")

        history = HistoryRepository.get_user_history(user_id=1, page=1, page_size=10)
        self.assertTrue(history["total"] > 0)

if __name__ == "__main__":
    unittest.main()
