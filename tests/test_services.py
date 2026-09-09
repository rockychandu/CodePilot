"""
Python Unit Test Suite for AuthService & ProblemService
"""

import unittest
from codepilot.services.auth_service import AuthServicePython
from codepilot.services.problem_service import ProblemServicePython

class TestServices(unittest.TestCase):
    def setUp(self):
        self.auth_svc = AuthServicePython()
        self.prob_svc = ProblemServicePython()

    def test_login_success(self):
        user = self.auth_svc.login("alex.developer@codepilot.io", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "alex_dev")

    def test_registration(self):
        user = self.auth_svc.register("New User", "new_user", "new@codepilot.io", "secret123")
        self.assertEqual(user.email, "new@codepilot.io")
        self.assertEqual(user.xp, 100)

    def test_problem_retrieval(self):
        problems = self.prob_svc.get_all(difficulty="easy")
        self.assertTrue(len(problems) >= 1)
        self.assertEqual(problems[0].id, "prob_1")

if __name__ == "__main__":
    unittest.main()
