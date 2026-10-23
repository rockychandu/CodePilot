import unittest
from backend.execution.pipe_multiplexer import PipeMultiplexer

class TestPipeMultiplexer(unittest.TestCase):
    def test_under_limit(self):
        text = "Hello world!"
        res, trunc = PipeMultiplexer.clamp_output(text, max_bytes=100)
        self.assertEqual(res, text)
        self.assertFalse(trunc)

    def test_over_limit_truncation(self):
        text = "A" * 200
        res, trunc = PipeMultiplexer.clamp_output(text, max_bytes=50)
        self.assertTrue(trunc)
        self.assertIn("[Output truncated", res)

    def test_empty_input(self):
        res, trunc = PipeMultiplexer.clamp_output("", max_bytes=50)
        self.assertEqual(res, "")
        self.assertFalse(trunc)

if __name__ == "__main__":
    unittest.main()
