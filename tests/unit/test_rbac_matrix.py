import unittest
from backend.auth.rbac_matrix import RBACMatrix

class TestRBACMatrix(unittest.TestCase):
    def test_admin_wildcard(self):
        self.assertTrue(RBACMatrix.has_permission("ADMIN", "any:arbitrary:permission"))
        self.assertTrue(RBACMatrix.has_permission("ADMIN", "system:kill"))

    def test_user_permissions(self):
        self.assertTrue(RBACMatrix.has_permission("USER", "problems:submit"))
        self.assertTrue(RBACMatrix.has_permission("USER", "projects:create"))
        self.assertFalse(RBACMatrix.has_permission("USER", "system:kill"))

    def test_guest_restrictions(self):
        self.assertTrue(RBACMatrix.has_permission("GUEST", "problems:view"))
        self.assertFalse(RBACMatrix.has_permission("GUEST", "problems:submit"))
        self.assertFalse(RBACMatrix.has_permission("GUEST", "projects:create"))

if __name__ == "__main__":
    unittest.main()
