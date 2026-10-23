"""
Python Exception Traceback Clean Formatter
"""
import re

class PythonDiagnosticsParser:
    @staticmethod
    def extract_user_error(traceback_str: str) -> dict:
        if not traceback_str:
            return {"errorType": "Unknown", "message": "", "line": None}

        lines = [line.strip() for line in traceback_str.strip().splitlines() if line.strip()]
        last_line = lines[-1] if lines else ""

        error_type = "Exception"
        error_msg = last_line
        if ":" in last_line:
            parts = last_line.split(":", 1)
            error_type = parts[0].strip()
            error_msg = parts[1].strip()

        line_num = None
        for l in reversed(lines):
            match = re.search(r"line\s+(\d+)", l, re.IGNORECASE)
            if match:
                line_num = int(match.group(1))
                break

        return {
            "errorType": error_type,
            "message": error_msg,
            "line": line_num
        }
