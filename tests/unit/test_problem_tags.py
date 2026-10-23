import unittest
from backend.problems.tags import ProblemTagTaxonomy

class TestProblemTags(unittest.TestCase):
    def test_normalize_tag(self):
        self.assertEqual(ProblemTagTaxonomy.normalize_tag("  dynamic   programming "), "Dynamic Programming")

    def test_category_lookup(self):
        self.assertEqual(ProblemTagTaxonomy.get_category_for_tag("Dynamic Programming"), "Algorithms")
        self.assertEqual(ProblemTagTaxonomy.get_category_for_tag("Trees"), "Data Structures")
        self.assertEqual(ProblemTagTaxonomy.get_category_for_tag("UnknownTag"), "General")

    def test_list_all(self):
        tags = ProblemTagTaxonomy.list_all_tags()
        self.assertTrue(len(tags) >= 15)
        self.assertIn("Binary Search", tags)

if __name__ == "__main__":
    unittest.main()
