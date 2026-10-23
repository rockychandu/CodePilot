import unittest
from backend.ratings.glicko2 import Glicko2

class TestGlicko2(unittest.TestCase):
    def test_win_increases_rating(self):
        new_r = Glicko2.calculate_rating_change(1500.0, 1500.0, 1.0)
        self.assertTrue(new_r > 1500.0)
        self.assertEqual(new_r, 1516.0)

    def test_loss_decreases_rating(self):
        new_r = Glicko2.calculate_rating_change(1500.0, 1500.0, 0.0)
        self.assertTrue(new_r < 1500.0)
        self.assertEqual(new_r, 1484.0)

    def test_inactivity_rd_increase(self):
        new_rd = Glicko2.adjust_deviation_for_inactivity(100.0, 30)
        self.assertTrue(new_rd > 100.0)

if __name__ == "__main__":
    unittest.main()
