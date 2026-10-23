import unittest
from backend.judge.diff_analyzer import DiffAnalyzer

class TestDiffAnalyzer(unittest.TestCase):
    def test_exact_match(self):
        res = DiffAnalyzer.compare("42\nhello", "42\nhello")
        self.assertTrue(res["isMatch"])
        self.assertEqual(res["diffCount"], 0)

    def test_mismatch(self):
        res = DiffAnalyzer.compare("42\nworld", "42\nword")
        self.assertFalse(res["isMatch"])
        self.assertEqual(res["diffCount"], 1)
        self.assertEqual(res["diffs"][0]["line"], 2)

    def test_empty_comparison(self):
        res = DiffAnalyzer.compare("", "")
        self.assertTrue(res["isMatch"])

if __name__ == "__main__":
    unittest.main()
