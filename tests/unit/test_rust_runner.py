import unittest
from backend.compiler.rust_runner import RustRunnerConfig

class TestRustRunner(unittest.TestCase):
    def test_optimized_args(self):
        args = RustRunnerConfig.build_compile_args("main.rs", "main.exe", "2021", True)
        self.assertIn("--edition=2021", args)
        self.assertIn("opt-level=3", args)
        self.assertEqual(args[-1], "main.rs")

    def test_debug_args(self):
        args = RustRunnerConfig.build_compile_args("main.rs", "main.exe", "2024", False)
        self.assertIn("--edition=2024", args)
        self.assertNotIn("opt-level=3", args)

    def test_output_flag(self):
        args = RustRunnerConfig.build_compile_args("src.rs", "bin_out")
        idx = args.index("-o")
        self.assertEqual(args[idx + 1], "bin_out")

if __name__ == "__main__":
    unittest.main()
