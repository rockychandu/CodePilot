import unittest
from backend.compiler.python_diagnostics import PythonDiagnosticsParser

class TestPythonDiagnostics(unittest.TestCase):
    def test_extract_syntax_error(self):
        tb = """  File "solution.py", line 7
    if x == 5
            ^
SyntaxError: expected ':'"""
        res = PythonDiagnosticsParser.extract_user_error(tb)
        self.assertEqual(res["errorType"], "SyntaxError")
        self.assertEqual(res["line"], 7)
        self.assertIn("expected ':'", res["message"])

    def test_extract_runtime_zero_division(self):
        tb = """Traceback (most recent call last):
  File "solution.py", line 12, in <module>
    ans = 10 / 0
ZeroDivisionError: division by zero"""
        res = PythonDiagnosticsParser.extract_user_error(tb)
        self.assertEqual(res["errorType"], "ZeroDivisionError")
        self.assertEqual(res["line"], 12)
        self.assertEqual(res["message"], "division by zero")

    def test_empty_traceback(self):
        res = PythonDiagnosticsParser.extract_user_error("")
        self.assertIsNone(res["line"])

if __name__ == "__main__":
    unittest.main()
