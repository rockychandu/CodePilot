import unittest
from backend.problems.editorial import EditorialValidator

class TestEditorialValidator(unittest.TestCase):
    def test_valid_editorial(self):
        text = """## Intuition
Use a hash map.
## Complexity
Time: O(N), Space: O(N)
## Solution
```python
def solve(): pass
```"""
        res = EditorialValidator.validate_editorial(text)
        self.assertTrue(res["isValid"])
        self.assertEqual(len(res["missingSections"]), 0)

    def test_missing_sections(self):
        text = "# Intuition\nJust guess."
        res = EditorialValidator.validate_editorial(text)
        self.assertFalse(res["isValid"])
        self.assertIn("Complexity", res["missingSections"])

    def test_empty(self):
        res = EditorialValidator.validate_editorial("")
        self.assertFalse(res["isValid"])

if __name__ == "__main__":
    unittest.main()
