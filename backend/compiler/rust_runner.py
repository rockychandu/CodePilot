"""
Rust Compiler Runner Configuration
"""
class RustRunnerConfig:
    @staticmethod
    def build_compile_args(source_path: str, output_path: str, edition: str = "2021", optimize: bool = True) -> list:
        args = ["rustc", f"--edition={edition}"]
        if optimize:
            args.extend(["-C", "opt-level=3"])
        args.extend(["-o", output_path, source_path])
        return args
