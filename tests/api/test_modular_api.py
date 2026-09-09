"""
Automated Integration Tests for Modular REST API Endpoints (/api/v1/*)
"""

import os
import sys
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.app import app

class TestModularApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        resp = self.client.get("/api/v1/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "HEALTHY")

    def test_ready_endpoint(self):
        resp = self.client.get("/ready")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "READY")

    def test_runtime_languages_endpoint(self):
        resp = self.client.get("/api/v1/runtime/languages")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        lang_ids = [l["id"] for l in data]
        self.assertIn("python", lang_ids)

    def test_python_code_execution_endpoint(self):
        payload = {
            "language": "python",
            "sourceCode": "print('CodePilot Integration Test Passed')",
            "stdin": ""
        }
        resp = self.client.post("/api/v1/execution/run", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["status"], "ACCEPTED")
        self.assertIn("CodePilot Integration Test Passed", data["stdout"])

    def test_problems_endpoint(self):
        resp = self.client.get("/api/v1/problems")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_contests_endpoint(self):
        resp = self.client.get("/api/v1/contests")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)

    def test_courses_endpoint(self):
        resp = self.client.get("/api/v1/courses")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)

    def test_global_search_endpoint(self):
        resp = self.client.get("/api/v1/search?q=Sum")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("problems", data)

    def test_ai_review_endpoint(self):
        payload = {
            "language": "python",
            "sourceCode": "def add(a, b):\n    return a + b"
        }
        resp = self.client.post("/api/v1/ai/review", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("qualityScore", data)

if __name__ == "__main__":
    unittest.main()
