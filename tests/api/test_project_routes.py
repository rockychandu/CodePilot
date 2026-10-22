"""
Integration Tests for Project Workspace REST API Endpoints
"""

import unittest
import json
import uuid
from backend.app import app


class TestProjectRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        uname = f"proj_user_{uuid.uuid4().hex[:8]}"
        email = f"{uname}@example.com"
        reg_resp = self.client.post("/api/v1/auth/register", json={
            "username": uname,
            "email": email,
            "password": "Password@123",
            "displayName": "Workspace Dev"
        })
        self.token = reg_resp.json["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_project_crud_flow(self):
        # 1. Create project
        create_resp = self.client.post("/api/v1/projects", headers=self.headers, json={
            "title": "API Test Project",
            "description": "Integration test project",
            "language": "python",
            "template": "cli"
        })
        self.assertEqual(create_resp.status_code, 201)
        pid = create_resp.json["id"]

        # 2. Get project
        get_resp = self.client.get(f"/api/v1/projects/{pid}", headers=self.headers)
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json["title"], "API Test Project")

        # 3. Rename project
        rename_resp = self.client.patch(f"/api/v1/projects/{pid}", headers=self.headers, json={
            "title": "API Test Project (Updated)"
        })
        self.assertEqual(rename_resp.status_code, 200)
        self.assertEqual(rename_resp.json["title"], "API Test Project (Updated)")

        # 4. Duplicate project
        dup_resp = self.client.post(f"/api/v1/projects/{pid}/duplicate", headers=self.headers)
        self.assertEqual(dup_resp.status_code, 201)
        dup_id = dup_resp.json["id"]
        self.assertIn("Copy", dup_resp.json["title"])

        # 5. Export project
        exp_resp = self.client.get(f"/api/v1/projects/{pid}/export", headers=self.headers)
        self.assertEqual(exp_resp.status_code, 200)
        self.assertEqual(exp_resp.json["version"], "1.0")

        # 6. Delete file
        del_file_resp = self.client.delete(f"/api/v1/projects/{pid}/files/README.md", headers=self.headers)
        self.assertEqual(del_file_resp.status_code, 200)

        # 7. Delete projects
        del_resp = self.client.delete(f"/api/v1/projects/{pid}", headers=self.headers)
        self.assertEqual(del_resp.status_code, 200)

        del_dup_resp = self.client.delete(f"/api/v1/projects/{dup_id}", headers=self.headers)
        self.assertEqual(del_dup_resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
