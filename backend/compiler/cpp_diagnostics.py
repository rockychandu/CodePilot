"""
C++ Compiler Diagnostic Log Parser
"""
import re

class CppDiagnosticsParser:
    GCC_ERROR_REGEX = re.compile(r"^([^:]+):(\d+):(\d+):\s*(error|warning|fatal error):\s*(.*)$", re.MULTILINE)

    @classmethod
    def parse(cls, compiler_output: str) -> list:
        diagnostics = []
        if not compiler_output:
            return diagnostics
        for match in cls.GCC_ERROR_REGEX.finditer(compiler_output):
            diagnostics.append({
                "file": match.group(1),
                "line": int(match.group(2)),
                "column": int(match.group(3)),
                "severity": match.group(4).upper(),
                "message": match.group(5).strip()
            })
        return diagnostics
