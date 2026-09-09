"""
API Tests for CodePilot /api/v1 REST Endpoints
"""

import unittest
import json
import uuid
from backend.app import app


class TestAPIv1(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_and_ready(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["status"], "HEALTHY")

        resp_ready = self.client.get("/ready")
        self.assertEqual(resp_ready.status_code, 200)
        self.assertEqual(resp_ready.json["status"], "READY")

    def test_auth_and_profile_flow(self):
        uname = f"api_user_{uuid.uuid4().hex[:8]}"
        email = f"{uname}@example.com"
        password = "Password@123"

        # 1. Register
        reg_resp = self.client.post("/api/v1/auth/register", json={
            "username": uname,
            "email": email,
            "password": password,
            "displayName": "API Tester"
        })
        self.assertEqual(reg_resp.status_code, 201)
        token = reg_resp.json["token"]

        # 2. Get Profile with Bearer token
        prof_resp = self.client.get("/api/v1/profile", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(prof_resp.status_code, 200)
        self.assertEqual(prof_resp.json["username"], uname)

        # 3. Update Profile
        update_resp = self.client.put("/api/v1/profile", headers={"Authorization": f"Bearer {token}"}, json={
            "displayName": "Updated API Tester",
            "bio": "API testing suite."
        })
        self.assertEqual(update_resp.status_code, 200)
        self.assertEqual(update_resp.json["profile"]["displayName"], "Updated API Tester")

    def test_code_execution_api(self):
        resp = self.client.post("/api/v1/execution/run", json={
            "language": "python",
            "sourceCode": "print('API Execution Test')"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["status"], "ACCEPTED")
        self.assertIn("API Execution Test", resp.json["stdout"])

    def test_problems_and_leaderboards(self):
        p_resp = self.client.get("/api/v1/problems")
        self.assertEqual(p_resp.status_code, 200)
        self.assertTrue(len(p_resp.json) >= 1)

        l_resp = self.client.get("/api/v1/leaderboards?type=GLOBAL")
        self.assertEqual(l_resp.status_code, 200)
        self.assertTrue(isinstance(l_resp.json, list))

    def test_courses_and_contests(self):
        c_resp = self.client.get("/api/v1/courses")
        self.assertEqual(c_resp.status_code, 200)
        self.assertTrue(len(c_resp.json) >= 1)

        ct_resp = self.client.get("/api/v1/contests")
        self.assertEqual(ct_resp.status_code, 200)
        self.assertTrue(len(ct_resp.json) >= 1)

    def test_pilot_ai_routes(self):
        rev_resp = self.client.post("/api/v1/ai/review", json={
            "language": "python",
            "sourceCode": "def f(x):\n    return x * 2\n"
        })
        self.assertEqual(rev_resp.status_code, 200)
        self.assertIn("Pilot AI Code Review", rev_resp.json["output"])

        comp_resp = self.client.post("/api/v1/ai/complexity", json={
            "language": "python",
            "sourceCode": "for i in range(10):\n    print(i)"
        })
        self.assertEqual(comp_resp.status_code, 200)
        self.assertEqual(comp_resp.json["time"], "O(N)")


if __name__ == "__main__":
    unittest.main()
