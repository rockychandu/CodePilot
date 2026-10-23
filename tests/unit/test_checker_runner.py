import unittest
from backend.judge.checker_runner import CheckerRunner

class TestCheckerRunner(unittest.TestCase):
    def test_accepted(self):
        res = CheckerRunner.parse_checker_result(0, "ok solution valid")
        self.assertEqual(res["verdict"], "ACCEPTED")
        self.assertEqual(res["message"], "ok solution valid")

    def test_wrong_answer(self):
        res = CheckerRunner.parse_checker_result(1, "cycle detected in path")
        self.assertEqual(res["verdict"], "WRONG_ANSWER")

    def test_checker_crash(self):
        res = CheckerRunner.parse_checker_result(139, "")
        self.assertEqual(res["verdict"], "CHECKER_ERROR")

if __name__ == "__main__":
    unittest.main()
