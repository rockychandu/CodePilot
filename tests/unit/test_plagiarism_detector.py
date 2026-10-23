import unittest
from backend.judge.plagiarism_detector import PlagiarismDetector

class TestPlagiarismDetector(unittest.TestCase):
    def test_identical_code(self):
        code = "def two_sum(nums, target):\n    d = {}\n    for i, x in enumerate(nums): pass"
        sim = PlagiarismDetector.calculate_similarity(code, code)
        self.assertEqual(sim, 1.0)

    def test_completely_different_code(self):
        c1 = "class Solution: def dfs(self): pass"
        c2 = "int main() { printf('hello'); return 0; }"
        sim = PlagiarismDetector.calculate_similarity(c1, c2)
        self.assertTrue(sim < 0.2)

    def test_empty(self):
        self.assertEqual(PlagiarismDetector.calculate_similarity("", ""), 0.0)

if __name__ == "__main__":
    unittest.main()
