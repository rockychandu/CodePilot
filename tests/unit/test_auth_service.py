"""
Unit tests for CodePilot AuthService
"""

import unittest
import uuid
from codepilot.db.connection import init_db
from codepilot.services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_password_strength_validation(self):
        self.assertFalse(AuthService.validate_password_strength("short")[0])
        self.assertFalse(AuthService.validate_password_strength("nouppercase123")[0])
        self.assertFalse(AuthService.validate_password_strength("NOLOWERCASE123")[0])
        self.assertFalse(AuthService.validate_password_strength("NoDigitsHere!")[0])
        self.assertTrue(AuthService.validate_password_strength("ValidPass@123")[0])

    def test_email_validation(self):
        self.assertTrue(AuthService.validate_email("user@example.com"))
        self.assertTrue(AuthService.validate_email("john.doe@sub.domain.co"))
        self.assertFalse(AuthService.validate_email("invalid-email"))
        self.assertFalse(AuthService.validate_email("@missinguser.com"))

    def test_username_validation(self):
        self.assertTrue(AuthService.validate_username("alex_dev")[0])
        self.assertFalse(AuthService.validate_username("ab")[0])  # too short
        self.assertFalse(AuthService.validate_username("invalid user name")[0])  # spaces
        self.assertFalse(AuthService.validate_username("user@name!")[0])  # special chars

    def test_user_registration_and_authentication(self):
        uname = f"user_{uuid.uuid4().hex[:8]}"
        email = f"{uname}@example.com"
        password = "Password@123"

        # Register
        ok, res = AuthService.register_user(uname, email, password, "Test Display")
        self.assertTrue(ok)
        self.assertIn("token", res)
        self.assertEqual(res["user"]["username"], uname)

        # Duplicate register should fail
        dup_ok, dup_msg = AuthService.register_user(uname, f"other_{email}", password)
        self.assertFalse(dup_ok)
        self.assertEqual(dup_msg, "Username is already taken.")

        # Authenticate with username
        auth_ok, auth_res = AuthService.authenticate_user(uname, password)
        self.assertTrue(auth_ok)
        self.assertIn("token", auth_res)

        # Authenticate with email
        auth_email_ok, _ = AuthService.authenticate_user(email, password)
        self.assertTrue(auth_email_ok)

        # Authenticate with wrong password
        fail_ok, _ = AuthService.authenticate_user(uname, "WrongPass@123")
        self.assertFalse(fail_ok)

    def test_password_reset_flow(self):
        uname = f"reset_{uuid.uuid4().hex[:8]}"
        email = f"{uname}@example.com"
        AuthService.register_user(uname, email, "OldPassword@123")

        # Request reset
        ok, token = AuthService.request_password_reset(email)
        self.assertTrue(ok)

        # Execute reset
        new_pwd = "NewPassword@999"
        res_ok, msg = AuthService.reset_password(token, new_pwd)
        self.assertTrue(res_ok)

        # Verify old password fails and new password works
        old_auth, _ = AuthService.authenticate_user(uname, "OldPassword@123")
        self.assertFalse(old_auth)
        new_auth, _ = AuthService.authenticate_user(uname, new_pwd)
        self.assertTrue(new_auth)


if __name__ == "__main__":
    unittest.main()
