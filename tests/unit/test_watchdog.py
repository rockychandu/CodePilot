import unittest
from backend.sandbox.watchdog import ExecutionWatchdog

class TestExecutionWatchdog(unittest.TestCase):
    def test_within_time(self):
        res = ExecutionWatchdog.check_timeout(0.5, 2.0)
        self.assertFalse(res["isTimeout"])
        self.assertEqual(res["status"], "COMPLETED")

    def test_timeout_triggered(self):
        res = ExecutionWatchdog.check_timeout(2.1, 2.0)
        self.assertTrue(res["isTimeout"])
        self.assertEqual(res["status"], "TIME_LIMIT_EXCEEDED")

    def test_max_limit_clamp(self):
        res = ExecutionWatchdog.check_timeout(11.0, 30.0)
        self.assertEqual(res["limitSec"], 10.0)
        self.assertTrue(res["isTimeout"])

if __name__ == "__main__":
    unittest.main()
