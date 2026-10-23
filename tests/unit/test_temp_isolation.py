import unittest
import os
from backend.sandbox.temp_isolation import IsolatedWorkspace

class TestIsolatedWorkspace(unittest.TestCase):
    def test_directory_lifecycle(self):
        path = None
        with IsolatedWorkspace() as ws:
            path = ws.path
            self.assertTrue(os.path.exists(path))
            fpath = ws.write_file("test.py", "print('hello')")
            self.assertTrue(os.path.exists(fpath))
        self.assertFalse(os.path.exists(path))

    def test_nested_file_creation(self):
        with IsolatedWorkspace() as ws:
            fpath = ws.write_file("sub/dir/module.py", "# code")
            self.assertTrue(os.path.exists(fpath))

    def test_content_integrity(self):
        with IsolatedWorkspace() as ws:
            fpath = ws.write_file("main.cpp", "int main() { return 0; }")
            with open(fpath, "r", encoding="utf-8") as f:
                self.assertIn("int main()", f.read())

if __name__ == "__main__":
    unittest.main()
