import unittest
from backend.storage.testcase_compression import TestCaseCompressor

class TestTestCaseCompression(unittest.TestCase):
    def test_small_text_uncompressed(self):
        small = "input: 1 2 3\noutput: 6"
        res, is_comp = TestCaseCompressor.compress_if_needed(small)
        self.assertFalse(is_comp)
        self.assertEqual(res, small)

    def test_large_text_roundtrip(self):
        large = "1000000\n" + "1 " * 2000
        comp, is_comp = TestCaseCompressor.compress_if_needed(large)
        self.assertTrue(is_comp)
        self.assertTrue(len(comp) < len(large))

        decomp = TestCaseCompressor.decompress(comp, True)
        self.assertEqual(decomp, large)

    def test_empty_string(self):
        res, is_comp = TestCaseCompressor.compress_if_needed("")
        self.assertFalse(is_comp)
        self.assertEqual(res, "")

if __name__ == "__main__":
    unittest.main()
