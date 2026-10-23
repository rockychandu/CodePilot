import unittest
from backend.middleware.security_headers import SecurityHeaders

class TestSecurityHeaders(unittest.TestCase):
    def test_apply_headers(self):
        resp = SecurityHeaders.apply_security_headers({"Content-Type": "application/json"})
        self.assertEqual(resp["X-Content-Type-Options"], "nosniff")
        self.assertEqual(resp["X-Frame-Options"], "DENY")
        self.assertEqual(resp["Content-Type"], "application/json")

    def test_origin_validation(self):
        allowed = ["https://codepilot.dev", "http://localhost:3000"]
        self.assertTrue(SecurityHeaders.is_allowed_origin("https://codepilot.dev", allowed))
        self.assertTrue(SecurityHeaders.is_allowed_origin("http://localhost:3000/", allowed))
        self.assertFalse(SecurityHeaders.is_allowed_origin("https://evil.com", allowed))

    def test_wildcard_origin(self):
        self.assertTrue(SecurityHeaders.is_allowed_origin("https://anywhere.org", ["*"]))

if __name__ == "__main__":
    unittest.main()
