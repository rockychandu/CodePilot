"""
Unit and Integration Tests for CodePilot Authentication and Session System.
"""

import os
import sys
import unittest
import json

# Ensure repository root is on sys.path
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from backend.app import app
from backend.auth.service import AuthService
from backend.auth.password import hash_password, verify_password, evaluate_password_strength
from backend.auth.tokens import create_access_token, verify_access_token
from backend.auth.rate_limit import AuthRateLimiter
from codepilot.db.connection import get_db_session
from codepilot.db.models import User, Profile, UserSession, ActivityHistory, PasswordReset, EmailVerification

class TestAuthSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def setUp(self):
        self.username = f"test_user_{os.urandom(4).hex()}"
        self.email = f"{self.username}@testmail.com"
        self.password = "StrongP@ssw0rd!2026"

    def test_password_strength_evaluator(self):
        weak = evaluate_password_strength("12345")
        self.assertFalse(weak["isAcceptable"])
        self.assertEqual(weak["label"], "Weak")

        strong = evaluate_password_strength("CodePilot#2026!Secure")
        self.assertTrue(strong["isAcceptable"])
        self.assertEqual(strong["label"], "Strong")

    def test_password_hashing_and_verification(self):
        salt = os.urandom(16).hex()
        pw = "SecretKey#999"
        pw_hash = hash_password(pw, salt)
        
        self.assertTrue(verify_password(pw, salt, pw_hash))
        self.assertFalse(verify_password("WrongKey#999", salt, pw_hash))

    def test_jwt_token_lifecycle(self):
        token = create_access_token(user_id=42, username="dev_tester", role="USER")
        self.assertIsInstance(token, str)
        self.assertTrue(len(token.split('.')) == 3)

        payload = verify_access_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload["user_id"], 42)
        self.assertEqual(payload["username"], "dev_tester")

        # Invalid token
        self.assertIsNone(verify_access_token("invalid.jwt.token"))

    def test_registration_and_login_flow(self):
        # 1. Register User
        res = self.client.post("/api/v1/auth/register", json={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "confirmPassword": self.password,
            "displayName": "Test Coder"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("token", data)
        self.assertIn("user", data)
        self.assertEqual(data["user"]["username"], self.username)

        # 2. Duplicate Registration Rejection
        dup_res = self.client.post("/api/v1/auth/register", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })
        self.assertEqual(dup_res.status_code, 400)
        dup_data = dup_res.get_json()
        self.assertFalse(dup_data["success"])

        # 3. Weak Password Rejection
        weak_res = self.client.post("/api/v1/auth/register", json={
            "username": f"weak_{self.username}",
            "email": f"weak_{self.email}",
            "password": "123"
        })
        self.assertEqual(weak_res.status_code, 400)

        # 4. Successful Login
        login_res = self.client.post("/api/v1/auth/login", json={
            "identifier": self.username,
            "password": self.password
        })
        self.assertEqual(login_res.status_code, 200)
        login_data = login_res.get_json()
        self.assertTrue(login_data["success"])
        token = login_data["token"]
        refresh_token = login_data["refreshToken"]

        # 5. Invalid Password Login
        bad_login = self.client.post("/api/v1/auth/login", json={
            "identifier": self.username,
            "password": "WrongPassword!999"
        })
        self.assertEqual(bad_login.status_code, 401)

        # 6. Current User /me Endpoint
        me_res = self.client.get("/api/v1/auth/me", headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.get_json()
        self.assertEqual(me_data["user"]["username"], self.username)

        # 7. Token Refresh
        ref_res = self.client.post("/api/v1/auth/refresh", json={
            "refreshToken": refresh_token
        })
        self.assertEqual(ref_res.status_code, 200)
        ref_data = ref_res.get_json()
        self.assertTrue(ref_data["success"])
        self.assertIn("token", ref_data)
        current_token = ref_data["token"]

        # 8. Password Change using refreshed token
        new_pwd = "UpdatedSecurePassword#2026!"
        change_res = self.client.put("/api/v1/auth/change-password", headers={
            "Authorization": f"Bearer {current_token}"
        }, json={
            "currentPassword": self.password,
            "newPassword": new_pwd
        })
        self.assertEqual(change_res.status_code, 200)

        # 9. Verify Login with New Password
        new_login = self.client.post("/api/v1/auth/login", json={
            "identifier": self.username,
            "password": new_pwd
        })
        self.assertEqual(new_login.status_code, 200)

    def test_password_reset_and_email_verification_flow(self):
        # Register user
        user_name = f"pwd_reset_{os.urandom(3).hex()}"
        user_email = f"{user_name}@example.com"
        _, reg_data = AuthService.register_user(user_name, user_email, "InitPassword#2026!")

        # Request password reset
        forgot_res = self.client.post("/api/v1/auth/forgot-password", json={"email": user_email})
        self.assertEqual(forgot_res.status_code, 200)

        # Retrieve reset token from DB
        with get_db_session() as db:
            reset_entry = db.query(PasswordReset).filter_by(user_id=reg_data["user"]["id"], is_used=False).order_by(PasswordReset.id.desc()).first()
            self.assertIsNotNone(reset_entry)
            reset_token = reset_entry.reset_token

        # Reset password via token
        new_pw = "ResetPassword#2026!Updated"
        reset_res = self.client.post("/api/v1/auth/reset-password", json={
            "token": reset_token,
            "password": new_pw
        })
        self.assertEqual(reset_res.status_code, 200)

        # Verify login with new password
        login_res = self.client.post("/api/v1/auth/login", json={
            "identifier": user_email,
            "password": new_pw
        })
        self.assertEqual(login_res.status_code, 200)

        # Test email verification
        resend_res = self.client.post("/api/v1/auth/resend-verification", json={"email": user_email})
        self.assertEqual(resend_res.status_code, 200)

        with get_db_session() as db:
            ver_entry = db.query(EmailVerification).filter_by(user_id=reg_data["user"]["id"], is_used=False).order_by(EmailVerification.id.desc()).first()
            self.assertIsNotNone(ver_entry)
            ver_token = ver_entry.verification_token

        ver_res = self.client.post("/api/v1/auth/verify-email", json={"token": ver_token})
        self.assertEqual(ver_res.status_code, 200)

    def test_rate_limiter_lockout(self):
        limiter = AuthRateLimiter(max_attempts=3, lockout_seconds=60)
        test_ip = f"192.168.1.{os.urandom(2).hex()}"
        user_id = f"brute_force_target_{os.urandom(2).hex()}"

        self.assertFalse(limiter.is_locked(test_ip, user_id))
        limiter.record_attempt(test_ip, user_id, False, "WRONG_PWD")
        limiter.record_attempt(test_ip, user_id, False, "WRONG_PWD")
        limiter.record_attempt(test_ip, user_id, False, "WRONG_PWD")
        
        # Should now be locked
        self.assertTrue(limiter.is_locked(test_ip, user_id))

        # Successful attempt resets counter
        limiter.record_attempt(test_ip, user_id, True)
        self.assertFalse(limiter.is_locked(test_ip, user_id))

    def test_user_history_isolation(self):
        # Create two distinct users
        u1_name = f"iso_u1_{os.urandom(3).hex()}"
        u2_name = f"iso_u2_{os.urandom(3).hex()}"
        pwd = "TestPassword#2026!"

        _, r1 = AuthService.register_user(u1_name, f"{u1_name}@mail.com", pwd)
        _, r2 = AuthService.register_user(u2_name, f"{u2_name}@mail.com", pwd)

        tok1 = r1["token"]
        tok2 = r2["token"]

        # Record activity for User 1
        with get_db_session() as db:
            act1 = ActivityHistory(
                user_id=r1["user"]["id"],
                activity_type="CODE_EXECUTION",
                title="Python Script Isolated",
                language="python"
            )
            db.add(act1)
            db.commit()

        # User 1 queries history
        res1 = self.client.get("/api/v1/history", headers={"Authorization": f"Bearer {tok1}"})
        self.assertEqual(res1.status_code, 200)
        items1 = res1.get_json().get("items", [])
        self.assertTrue(any(i["title"] == "Python Script Isolated" for i in items1))

        # User 2 queries history -> must NOT see User 1's activity
        res2 = self.client.get("/api/v1/history", headers={"Authorization": f"Bearer {tok2}"})
        self.assertEqual(res2.status_code, 200)
        items2 = res2.get_json().get("items", [])
        self.assertFalse(any(i["title"] == "Python Script Isolated" for i in items2))

if __name__ == "__main__":
    unittest.main()
