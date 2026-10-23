import unittest
from backend.execution.bundler import SourceBundler

class TestSourceBundler(unittest.TestCase):
    def test_pack_files(self):
        files = [
            {"filename": "main.py", "content": "print(1)"},
            {"filename": "/utils/math.py", "content": "def add(a, b): return a + b"}
        ]
        b = SourceBundler.pack(files)
        self.assertIn("main.py", b)
        self.assertIn("utils/math.py", b)
        self.assertEqual(b["main.py"], "print(1)")

    def test_find_entrypoint(self):
        b = {"helper.py": "# code", "main.py": "print(1)"}
        ep = SourceBundler.find_entrypoint(b, "python")
        self.assertEqual(ep, "main.py")

    def test_fallback_entrypoint(self):
        b = {"custom.py": "# code"}
        ep = SourceBundler.find_entrypoint(b, "python")
        self.assertEqual(ep, "custom.py")

if __name__ == "__main__":
    unittest.main()
