"""
Unit tests for CodePilot UserService
"""

import unittest
import uuid
from codepilot.db.connection import init_db, db_session
from codepilot.services.auth_service import AuthService
from codepilot.services.user_service import UserService


class TestUserService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        uname = f"u_{uuid.uuid4().hex[:8]}"
        email = f"{uname}@example.com"
        _, res = AuthService.register_user(uname, email, "Password@123", "Initial Name")
        self.user_id = res["user"]["id"]
        self.username = uname

    def test_get_profile(self):
        profile = UserService.get_profile_by_id(self.user_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile["username"], self.username)
        self.assertEqual(profile["profile"]["displayName"], "Initial Name")

    def test_update_profile(self):
        ok, updated = UserService.update_profile(self.user_id, {
            "displayName": "Updated Super Dev",
            "bio": "Expert algorithm designer.",
            "primaryLanguage": "C++"
        })
        self.assertTrue(ok)
        self.assertEqual(updated["profile"]["displayName"], "Updated Super Dev")
        self.assertEqual(updated["profile"]["primaryLanguage"], "C++")

    def test_xp_award_and_leveling(self):
        prof = UserService.award_xp(self.user_id, 5000)
        self.assertTrue(prof["xp"] >= 5000)
        self.assertTrue(prof["level"] > 1)

    def test_isolated_activity_history(self):
        # Add 5 events
        for i in range(5):
            UserService.add_user_activity(
                user_id=self.user_id,
                activity_type="EXECUTION",
                title=f"Execution Test {i}",
                language="python",
                status="ACCEPTED"
            )

        history = UserService.get_user_activity_history(self.user_id, page=1, page_size=10)
        self.assertTrue(history["total"] >= 5)
        self.assertTrue(len(history["items"]) >= 5)


if __name__ == "__main__":
    unittest.main()
