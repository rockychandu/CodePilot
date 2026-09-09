"""
Python Unit Test Suite for CodePilot AST Engine & Sandbox
"""

import unittest
from codepilot.engine.sandbox import PythonEngine

class TestPythonEngine(unittest.TestCase):
    def test_valid_syntax(self):
        code = "def add(a, b):\n    return a + b"
        valid, tree, err = PythonEngine.validate_syntax(code)
        self.assertTrue(valid)
        self.assertIsNone(err)

    def test_invalid_syntax(self):
        code = "def broken_func("
        valid, tree, err = PythonEngine.validate_syntax(code)
        self.assertFalse(valid)
        self.assertIsNotNone(err)

    def test_ast_analysis(self):
        code = "def two_sum(nums, target):\n    for i in range(len(nums)):\n        pass"
        analysis = PythonEngine.analyze_code(code)
        self.assertTrue(analysis["valid"])
        self.assertEqual(analysis["loops"], 1)
        self.assertEqual(analysis["functions"], 1)

    def test_simulated_execution(self):
        code = "print('Hello World')"
        result = PythonEngine.run_simulated(code)
        self.assertEqual(result["status"], "Accepted")
        self.assertEqual(result["exitCode"], 0)

if __name__ == "__main__":
    unittest.main()
