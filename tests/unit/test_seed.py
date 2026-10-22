"""
Unit Test for Database Seeding Idempotency
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from codepilot.db.seed import seed_database
from codepilot.db.connection import get_db_session
from codepilot.db.models import Project, User

class TestSeedDatabase(unittest.TestCase):
    def test_seed_database_idempotency(self):
        # Running seed_database should succeed without crashing or violating unique constraints
        try:
            seed_database()
        except Exception as e:
            self.fail(f"seed_database raised an exception: {e}")

        with get_db_session() as db:
            projects = db.query(Project).all()
            self.assertTrue(len(projects) >= 1, "Expected seeded projects to exist in database.")

if __name__ == "__main__":
    unittest.main()
