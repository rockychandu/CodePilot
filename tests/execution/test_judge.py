"""
Competitive Programming Submission Judge Tests
"""

import unittest
from codepilot.db.connection import init_db, db_session
from codepilot.db.models import Problem, User
from codepilot.judge.submission_judge import SubmissionJudge


class TestSubmissionJudge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_evaluate_two_sum_accepted(self):
        db = db_session()
        prob = db.query(Problem).filter_by(slug="two-sum").first()
        user = db.query(User).filter_by(username="admin").first()

        sol_code = """
import sys

def solve():
    lines = sys.stdin.read().strip().split('\\n')
    if not lines or len(lines) < 2:
        return
    import ast
    nums = ast.literal_eval(lines[0])
    target = int(lines[1])
    lookup = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in lookup:
            print([lookup[diff], i])
            return
        lookup[n] = i

solve()
"""
        res = SubmissionJudge.evaluate_submission(
            user_id=user.id,
            problem_id=prob.id,
            language="python",
            source_code=sol_code
        )

        self.assertEqual(res["status"], "Accepted")
        self.assertEqual(res["passedTests"], res["totalTests"])
        self.assertTrue(len(res["testResults"]) >= 2)

    def test_evaluate_two_sum_wrong_answer(self):
        db = db_session()
        prob = db.query(Problem).filter_by(slug="two-sum").first()
        user = db.query(User).filter_by(username="admin").first()

        sol_code = "print([99, 99])"
        res = SubmissionJudge.evaluate_submission(
            user_id=user.id,
            problem_id=prob.id,
            language="python",
            source_code=sol_code
        )

        self.assertEqual(res["status"], "Wrong Answer")


if __name__ == "__main__":
    unittest.main()
