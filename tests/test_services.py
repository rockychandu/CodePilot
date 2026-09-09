"""
Unit Test Suite for CodePilot Core Services
"""

import unittest
import uuid
from codepilot.db.connection import init_db
from codepilot.services.auth_service import AuthService
from codepilot.services.problem_service import ProblemService


# Backwards compatibility wrapper
class AuthServicePython:
    def login(self, identifier, password):
        ok, res = AuthService.authenticate_user(identifier, password)
        if ok:
            class DummyUser:
                def __init__(self, d):
                    self.username = d["username"]
                    self.email = d["email"]
                    self.xp = d.get("profile", {}).get("xp", 100)
            return DummyUser(res["user"])
        return None

    def register(self, display_name, username, email, password):
        ok, res = AuthService.register_user(username, email, password, display_name)
        if ok:
            class DummyUser:
                def __init__(self, d):
                    self.username = d["username"]
                    self.email = d["email"]
                    self.xp = d.get("profile", {}).get("xp", 100)
            return DummyUser(res["user"])
        return None


class ProblemServicePython:
    def get_all(self, difficulty=None):
        probs = ProblemService.get_all_problems(difficulty=difficulty)
        class DummyProb:
            def __init__(self, p):
                self.id = f"prob_{p['id']}"
                self.title = p["title"]
        return [DummyProb(p) for p in probs]


class TestServices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        self.auth_svc = AuthServicePython()
        self.prob_svc = ProblemServicePython()

    def test_registration_and_login(self):
        uname = f"u_{uuid.uuid4().hex[:8]}"
        email = f"{uname}@codepilot.io"
        user = self.auth_svc.register("New User", uname, email, "SecretPassword@123")
        self.assertIsNotNone(user)
        self.assertEqual(user.email, email)

        logged = self.auth_svc.login(uname, "SecretPassword@123")
        self.assertIsNotNone(logged)
        self.assertEqual(logged.username, uname)

    def test_problem_retrieval(self):
        problems = self.prob_svc.get_all(difficulty="Easy")
        self.assertTrue(len(problems) >= 1)
        self.assertTrue(problems[0].id.startswith("prob_"))


if __name__ == "__main__":
    unittest.main()
