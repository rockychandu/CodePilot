import unittest
from backend.judge.rejudge_service import RejudgeService

class TestRejudgeService(unittest.TestCase):
    def test_batch_prep(self):
        batch = RejudgeService.prepare_rejudge_batch([1, 2, 3])
        self.assertEqual(len(batch), 3)
        self.assertEqual(batch[0]["status"], "PENDING_REJUDGE")

    def test_score_delta(self):
        delta = RejudgeService.calculate_score_delta(80, 100)
        self.assertEqual(delta, 20)

    def test_score_delta_regression(self):
        delta = RejudgeService.calculate_score_delta(100, 60)
        self.assertEqual(delta, -40)

if __name__ == "__main__":
    unittest.main()
