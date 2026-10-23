import unittest
from backend.security.tiered_rate_limiter import TieredRateLimiter

class TestTieredRateLimiter(unittest.TestCase):
    def setUp(self):
        self.limiter = TieredRateLimiter()

    def test_allow_within_limit(self):
        allowed, _ = self.limiter.allow_request("user-1", tier="USER")
        self.assertTrue(allowed)

    def test_guest_quota_enforcement(self):
        client = "guest-ip-123"
        for _ in range(30):
            allowed, _ = self.limiter.allow_request(client, tier="GUEST")
            self.assertTrue(allowed)
        blocked, retry_after = self.limiter.allow_request(client, tier="GUEST")
        self.assertFalse(blocked)
        self.assertTrue(retry_after > 0)

    def test_admin_higher_quota(self):
        client = "admin-99"
        for _ in range(50):
            allowed, _ = self.limiter.allow_request(client, tier="ADMIN")
            self.assertTrue(allowed)

if __name__ == "__main__":
    unittest.main()
