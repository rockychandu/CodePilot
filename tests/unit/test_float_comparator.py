import unittest
from backend.judge.float_comparator import FloatComparator

class TestFloatComparator(unittest.TestCase):
    def test_exact_float(self):
        self.assertTrue(FloatComparator.compare_tokens("3.141592", "3.141592"))

    def test_within_epsilon(self):
        self.assertTrue(FloatComparator.compare_tokens("3.14159265", "3.14159260", epsilon=1e-6))

    def test_outside_epsilon(self):
        self.assertFalse(FloatComparator.compare_tokens("3.14", "3.15", epsilon=1e-4))

    def test_non_float_fallback(self):
        self.assertTrue(FloatComparator.compare_tokens("YES", "YES"))
        self.assertFalse(FloatComparator.compare_tokens("YES", "NO"))

if __name__ == "__main__":
    unittest.main()
