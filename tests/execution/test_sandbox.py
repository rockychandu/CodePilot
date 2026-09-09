"""
Execution Sandbox and Language Runner Unit & Integration Tests
"""

import unittest
from codepilot.engine.execution_sandbox import ExecutionSandbox
from codepilot.engine.runtime_manager import RuntimeManager


class TestExecutionSandbox(unittest.TestCase):
    def test_python_execution_accepted(self):
        code = "a = 5\nb = 7\nprint(f'SUM:{a + b}')"
        res = ExecutionSandbox.execute_code("python", code, timeout=5.0)
        self.assertEqual(res["status"], "ACCEPTED")
        self.assertIn("SUM:12", res["stdout"])
        self.assertEqual(res["exitCode"], 0)

    def test_python_stdin_handling(self):
        code = "name = input()\nprint(f'HELLO {name}')"
        res = ExecutionSandbox.execute_code("python", code, stdin_data="Alex", timeout=5.0)
        self.assertEqual(res["status"], "ACCEPTED")
        self.assertIn("HELLO Alex", res["stdout"])

    def test_python_runtime_error(self):
        code = "x = 10 / 0"
        res = ExecutionSandbox.execute_code("python", code, timeout=5.0)
        self.assertEqual(res["status"], "RUNTIME_ERROR")
        self.assertIn("ZeroDivisionError", res["stderr"])
        self.assertNotEqual(res["exitCode"], 0)

    def test_python_timeout(self):
        code = "import time\ntime.sleep(3)"
        res = ExecutionSandbox.execute_code("python", code, timeout=1.0)
        self.assertEqual(res["status"], "TIME_LIMIT_EXCEEDED")

    def test_empty_code_error(self):
        res = ExecutionSandbox.execute_code("python", "   \n\t  ")
        self.assertEqual(res["status"], "COMPILE_ERROR")

    def test_simulated_fallback_execution(self):
        cpp_code = '#include <iostream>\nint main() { std::cout << "Dynamic C++ Output" << std::endl; }'
        res = ExecutionSandbox.execute_code("cpp", cpp_code)
        self.assertEqual(res["status"], "ACCEPTED")
        self.assertTrue(len(res["stdout"]) > 0)


if __name__ == "__main__":
    unittest.main()
