import unittest
from backend.compiler.cpp_diagnostics import CppDiagnosticsParser

class TestCppDiagnostics(unittest.TestCase):
    def test_parse_gcc_error(self):
        log = "solution.cpp:14:5: error: expected ';' before 'return'"
        res = CppDiagnosticsParser.parse(log)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["line"], 14)
        self.assertEqual(res[0]["column"], 5)
        self.assertEqual(res[0]["severity"], "ERROR")
        self.assertIn("expected ';'", res[0]["message"])

    def test_parse_multiple_errors(self):
        log = """solution.cpp:5:1: error: unknown type name 'vector'
solution.cpp:10:3: warning: unused variable 'x' [-Wunused-variable]"""
        res = CppDiagnosticsParser.parse(log)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["severity"], "ERROR")
        self.assertEqual(res[1]["severity"], "WARNING")

    def test_empty_log(self):
        self.assertEqual(CppDiagnosticsParser.parse(""), [])

if __name__ == "__main__":
    unittest.main()
