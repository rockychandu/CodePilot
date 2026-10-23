import unittest
from backend.execution.memory_guard import MemoryGuard

class TestMemoryGuard(unittest.TestCase):
    def test_within_limits(self):
        res = MemoryGuard.evaluate_memory_usage(64 * 1024 * 1024, 256 * 1024 * 1024)
        self.assertFalse(res["isExceeded"])
        self.assertEqual(res["status"], "OK")

    def test_exceeded_limits(self):
        res = MemoryGuard.evaluate_memory_usage(300 * 1024 * 1024, 256 * 1024 * 1024)
        self.assertTrue(res["isExceeded"])
        self.assertEqual(res["status"], "MEMORY_LIMIT_EXCEEDED")
        self.assertIn("300.0MB", res["message"])

    def test_zero_usage(self):
        res = MemoryGuard.evaluate_memory_usage(0, 128 * 1024 * 1024)
        self.assertFalse(res["isExceeded"])

if __name__ == "__main__":
    unittest.main()
