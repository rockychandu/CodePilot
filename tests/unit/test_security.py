"""
Unit tests for CodePilot Security & Cryptography Utilities
"""

import unittest
import time
from datetime import timedelta
from codepilot.utils.security import (
    generate_salt, hash_password, verify_password,
    create_access_token, create_refresh_token, verify_token,
    _base64url_encode, _base64url_decode
)


class TestSecurityUtilities(unittest.TestCase):
    def test_salt_generation(self):
        salt1 = generate_salt()
        salt2 = generate_salt()
        self.assertEqual(len(salt1), 64)
        self.assertNotEqual(salt1, salt2)

    def test_password_hashing_and_verification(self):
        password = "SecurePassword@123"
        pw_hash, salt = hash_password(password)
        self.assertTrue(len(pw_hash) > 30)
        self.assertTrue(verify_password(password, pw_hash, salt))
        self.assertFalse(verify_password("WrongPassword", pw_hash, salt))

    def test_jwt_token_creation_and_verification(self):
        token = create_access_token(user_id=42, username="pilot_tester", role="ADMIN")
        payload = verify_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["user_id"], 42)
        self.assertEqual(payload["username"], "pilot_tester")
        self.assertEqual(payload["role"], "ADMIN")

    def test_jwt_token_tampering(self):
        token = create_access_token(user_id=42, username="pilot_tester", role="USER")
        parts = token.split(".")
        # Tamper payload
        tampered_token = f"{parts[0]}.eyJob21lIjoidHJ1ZSJ9.{parts[2]}"
        self.assertIsNone(verify_token(tampered_token))

    def test_jwt_token_expiration(self):
        token = create_access_token(user_id=1, username="test", expires_delta=timedelta(seconds=-10))
        self.assertIsNone(verify_token(token))

    def test_refresh_token_format(self):
        rt = create_refresh_token(user_id=99)
        self.assertTrue(rt.startswith("rt_99_"))
        self.assertTrue(len(rt) > 30)

    def test_base64url_roundtrip(self):
        original = b"CodePilot 2026 Production Security Test Data"
        encoded = _base64url_encode(original)
        decoded = _base64url_decode(encoded)
        self.assertEqual(decoded, original)


if __name__ == "__main__":
    unittest.main()
