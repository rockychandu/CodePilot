import unittest
from backend.auth.password_policy import PasswordPolicy

class TestPasswordPolicy(unittest.TestCase):
    def test_strong_password(self):
        res = PasswordPolicy.evaluate("SuperSecretDev@2026!")
        self.assertTrue(res["isValid"])
        self.assertEqual(res["strength"], "STRONG")
        self.assertTrue(res["entropyBits"] > 50)

    def test_weak_password_length(self):
        res = PasswordPolicy.evaluate("Short1!")
        self.assertFalse(res["isValid"])
        self.assertIn("at least 8 characters", res["issues"][0])

    def test_common_password_rejection(self):
        res = PasswordPolicy.evaluate("password")
        self.assertFalse(res["isValid"])
        self.assertIn("Password is too common.", res["issues"])

    def test_entropy_computation(self):
        ent = PasswordPolicy.calculate_entropy("abc")
        self.assertTrue(ent > 0)
        self.assertEqual(PasswordPolicy.calculate_entropy(""), 0.0)

if __name__ == "__main__":
    unittest.main()
