"""
Judge Verdict Test Case Diff Analyzer
"""
class DiffAnalyzer:
    @staticmethod
    def compare(expected: str, actual: str) -> dict:
        exp_lines = (expected or "").splitlines()
        act_lines = (actual or "").splitlines()

        is_match = exp_lines == act_lines
        diffs = []
        max_len = max(len(exp_lines), len(act_lines))
        for i in range(max_len):
            e = exp_lines[i] if i < len(exp_lines) else None
            a = act_lines[i] if i < len(act_lines) else None
            if e != a:
                diffs.append({
                    "line": i + 1,
                    "expected": e,
                    "actual": a
                })

        return {
            "isMatch": is_match,
            "diffCount": len(diffs),
            "diffs": diffs[:10],
            "expectedLineCount": len(exp_lines),
            "actualLineCount": len(act_lines)
        }
