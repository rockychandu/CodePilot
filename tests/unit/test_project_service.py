"""
Unit Tests for ProjectService
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.projects.project_service import ProjectService

class TestProjectService(unittest.TestCase):
    def test_project_service_lifecycle(self):
        # 1. Create project
        proj = ProjectService.create_project(
            user_id=1,
            title="Service Test Workspace",
            description="Created via ProjectService unit test",
            language="javascript",
            template="cli"
        )
        self.assertIsNotNone(proj)
        self.assertEqual(proj["title"], "Service Test Workspace")
        pid = proj["id"]

        # 2. Rename project
        renamed = ProjectService.rename_project(pid, user_id=1, title="Renamed Service Workspace")
        self.assertIsNotNone(renamed)
        self.assertEqual(renamed["title"], "Renamed Service Workspace")

        # 3. Duplicate project
        cloned = ProjectService.duplicate_project(pid, user_id=1)
        self.assertIsNotNone(cloned)
        self.assertIn("Copy", cloned["title"])

        # 4. Export project
        export_pkg = ProjectService.export_project(pid, user_id=1)
        self.assertIsNotNone(export_pkg)
        self.assertEqual(export_pkg["version"], "1.0")
        self.assertIn("files", export_pkg["project"])

        # 5. Delete file
        self.assertTrue(ProjectService.delete_project_file(pid, user_id=1, filename="README.md"))

        # 6. Delete projects
        self.assertTrue(ProjectService.delete_project(pid, user_id=1))
        self.assertTrue(ProjectService.delete_project(cloned["id"], user_id=1))

        # 7. Non-existent export
        self.assertIsNone(ProjectService.export_project(999999, user_id=1))

if __name__ == "__main__":
    unittest.main()
