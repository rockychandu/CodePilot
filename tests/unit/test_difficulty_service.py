import unittest
from backend.problems.difficulty_service import DifficultyService

class TestDifficultyService(unittest.TestCase):
    def test_easy_classification(self):
        res = DifficultyService.calculate_difficulty(100, 75)
        self.assertEqual(res["difficulty"], "EASY")
        self.assertEqual(res["acceptanceRate"], 75.0)

    def test_medium_classification(self):
        res = DifficultyService.calculate_difficulty(100, 45)
        self.assertEqual(res["difficulty"], "MEDIUM")

    def test_hard_classification(self):
        res = DifficultyService.calculate_difficulty(100, 15)
        self.assertEqual(res["difficulty"], "HARD")

    def test_zero_submissions(self):
        res = DifficultyService.calculate_difficulty(0, 0)
        self.assertEqual(res["difficulty"], "MEDIUM")
        self.assertEqual(res["acceptanceRate"], 0.0)

if __name__ == "__main__":
    unittest.main()
