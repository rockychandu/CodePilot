import unittest
import time
from backend.auth.token_blacklist import TokenBlacklist

class TestTokenBlacklist(unittest.TestCase):
    def setUp(self):
        self.bl = TokenBlacklist()

    def test_revoke_and_check(self):
        token_id = "test-jti-token-999"
        self.assertFalse(self.bl.is_revoked(token_id))
        self.bl.revoke(token_id, time.time() + 300)
        self.assertTrue(self.bl.is_revoked(token_id))

    def test_expired_token(self):
        token_id = "expired-token-111"
        self.bl.revoke(token_id, time.time() - 10)
        self.assertFalse(self.bl.is_revoked(token_id))

    def test_purge_routine(self):
        self.bl.revoke("t1", time.time() - 50)
        self.bl.revoke("t2", time.time() + 500)
        purged = self.bl.purge_expired()
        self.assertEqual(purged, 1)
        self.assertTrue(self.bl.is_revoked("t2"))

if __name__ == "__main__":
    unittest.main()
