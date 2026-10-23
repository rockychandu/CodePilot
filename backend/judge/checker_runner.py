"""
Special Judge Custom Checker Protocol
"""
class CheckerRunner:
    @staticmethod
    def parse_checker_result(exit_code: int, checker_stdout: str) -> dict:
        # Exit code 0 is AC, 1 is WA, 2 is PE, others are internal error
        verdict_map = {
            0: "ACCEPTED",
            1: "WRONG_ANSWER",
            2: "PRESENTATION_ERROR"
        }
        verdict = verdict_map.get(exit_code, "CHECKER_ERROR")
        msg = (checker_stdout or "").strip()
        return {
            "verdict": verdict,
            "exitCode": exit_code,
            "message": msg if msg else verdict
        }
