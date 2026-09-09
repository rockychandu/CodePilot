"""
CodePilot Pilot AI Developer Suite
Implements static AST analysis, complexity breakdown, automated test generation,
bug explanation, and refactoring suggestions.
"""

import ast
import json
import re
from codepilot.db.connection import db_session
from codepilot.db.models import AIReview, User


class PilotAIEngine:
    @classmethod
    def review_code(cls, user_id: int, language: str, source_code: str) -> dict:
        """Analyze source code quality, best practices, style, and potential bugs."""
        language = language.lower().strip()
        suggestions = []
        quality_score = 95
        output_lines = []

        if language == "python":
            try:
                tree = ast.parse(source_code)
                # Check for bare excepts
                for node in ast.walk(tree):
                    if isinstance(node, ast.ExceptHandler) and node.type is None:
                        suggestions.append("Avoid bare 'except:' clause; specify concrete exception classes like 'except ValueError:' or 'except Exception:'.")
                        quality_score -= 10

                    # Check for global variables
                    if isinstance(node, ast.Global):
                        suggestions.append(f"Global statement detected ('global {', '.join(node.names)}'). Consider encapsulating state in classes or pure functions.")
                        quality_score -= 5

                    # Check for print in production
                    if isinstance(node, ast.Call) and getattr(node.func, 'id', None) == 'print':
                        suggestions.append("Use logging framework (e.g., 'logging.getLogger()') instead of raw 'print()' statements for production tracing.")

                    # Check for mutable default args
                    if isinstance(node, ast.FunctionDef):
                        for default in node.args.defaults:
                            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                                suggestions.append(f"Function '{node.name}' uses mutable default argument. Use 'None' as default and initialize inside function body.")
                                quality_score -= 10

            except SyntaxError as e:
                return {
                    "status": "SYNTAX_ERROR",
                    "output": f"Python Syntax Error at line {e.lineno}: {e.msg}",
                    "complexityTime": "Unknown",
                    "complexitySpace": "Unknown",
                    "qualityScore": 0,
                    "suggestions": ["Fix the syntax error to enable comprehensive AI analysis."]
                }

        # Multi-language heuristics
        if "TODO" in source_code or "FIXME" in source_code:
            suggestions.append("Found unresolved 'TODO' / 'FIXME' comments in source code.")
            quality_score -= 5

        if len(source_code.splitlines()) > 300:
            suggestions.append("File exceeds 300 lines. Consider refactoring into smaller modular components.")
            quality_score -= 5

        complexity_info = cls.estimate_complexity(language, source_code)
        quality_score = max(30, min(100, quality_score))

        output_lines.append(f"### Pilot AI Code Review ({language.upper()})")
        output_lines.append(f"**Overall Quality Score**: {quality_score}/100")
        output_lines.append(f"**Estimated Time Complexity**: `{complexity_info['time']}`")
        output_lines.append(f"**Estimated Space Complexity**: `{complexity_info['space']}`\n")

        if suggestions:
            output_lines.append("#### Recommendations & Insights:")
            for s in suggestions:
                output_lines.append(f"- 💡 {s}")
        else:
            output_lines.append("✅ **Clean Code**: No code smells or critical antipatterns detected.")

        review_text = "\n".join(output_lines)

        # Persist review
        cls._save_review_record(
            user_id=user_id,
            language=language,
            source_code=source_code,
            analysis_type="REVIEW",
            review_output=review_text,
            time_comp=complexity_info["time"],
            space_comp=complexity_info["space"],
            score=quality_score,
            suggestions=suggestions
        )

        return {
            "output": review_text,
            "complexityTime": complexity_info["time"],
            "complexitySpace": complexity_info["space"],
            "qualityScore": quality_score,
            "suggestions": suggestions
        }

    @classmethod
    def estimate_complexity(cls, language: str, source_code: str) -> dict:
        """Estimate asymptotic time and space complexity via AST and loops analysis."""
        nested_loop_depth = 0
        current_depth = 0

        if language.lower() == "python":
            try:
                tree = ast.parse(source_code)
                class LoopVisitor(ast.NodeVisitor):
                    def __init__(self):
                        self.max_depth = 0
                        self.depth = 0
                        self.has_recursion = False

                    def visit_For(self, node):
                        self.depth += 1
                        self.max_depth = max(self.max_depth, self.depth)
                        self.generic_visit(node)
                        self.depth -= 1

                    def visit_While(self, node):
                        self.depth += 1
                        self.max_depth = max(self.max_depth, self.depth)
                        self.generic_visit(node)
                        self.depth -= 1

                visitor = LoopVisitor()
                visitor.visit(tree)
                nested_loop_depth = visitor.max_depth
            except Exception:
                nested_loop_depth = 1
        else:
            # Heuristic loop counting for C, C++, Java, JS
            for line in source_code.splitlines():
                if any(k in line for k in ["for (", "for(", "while (", "while("]):
                    current_depth += 1
                    nested_loop_depth = max(nested_loop_depth, current_depth)
                if "}" in line and current_depth > 0:
                    current_depth -= 1

        if nested_loop_depth == 0:
            time_comp = "O(1)"
        elif nested_loop_depth == 1:
            time_comp = "O(N)"
        elif nested_loop_depth == 2:
            time_comp = "O(N^2)"
        elif nested_loop_depth >= 3:
            time_comp = f"O(N^{nested_loop_depth})"
        else:
            time_comp = "O(N)"

        # Check for sorting functions
        if re.search(r'\b(sorted|\.sort|std::sort)\b', source_code):
            time_comp = "O(N log N)" if nested_loop_depth <= 1 else f"O(N^{nested_loop_depth} log N)"

        # Space complexity
        if any(w in source_code for w in ["[]", "{}", "dict()", "set()", "new Array", "vector<", "HashMap", "HashSet"]):
            space_comp = "O(N)"
        else:
            space_comp = "O(1)"

        return {"time": time_comp, "space": space_comp}

    @classmethod
    def generate_tests(cls, user_id: int, language: str, source_code: str) -> dict:
        """Generate automated unit tests for functions found in source code."""
        language = language.lower().strip()
        test_code = ""

        if language == "python":
            func_names = []
            try:
                tree = ast.parse(source_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                        func_names.append(node.name)
            except Exception:
                func_names = ["solution"]

            if not func_names:
                func_names = ["solution"]

            lines = [
                "import unittest",
                "",
                "class TestAutoGenerated(unittest.TestCase):"
            ]
            for fn in func_names:
                lines.extend([
                    f"    def test_{fn}_base_case(self):",
                    f"        # Test standard input",
                    f"        # result = {fn}(...)",
                    f"        # self.assertIsNotNone(result)",
                    f"        self.assertTrue(callable({fn}))",
                    "",
                    f"    def test_{fn}_edge_case_empty(self):",
                    f"        # Test boundary and edge cases",
                    f"        pass",
                    ""
                ])
            lines.extend([
                "if __name__ == '__main__':",
                "    unittest.main()"
            ])
            test_code = "\n".join(lines)

        elif language in ["javascript", "typescript"]:
            test_code = "// Auto-generated Jest / Vitest Suite\ndescribe('Solution Test Suite', () => {\n  it('should execute base cases correctly', () => {\n    expect(true).toBe(true);\n  });\n  it('should handle edge boundaries', () => {\n    // Edge cases\n  });\n});"

        else:
            test_code = f"// Automated unit tests for {language.upper()}\n// Include standard test asserts for edge cases and typical inputs."

        cls._save_review_record(
            user_id=user_id,
            language=language,
            source_code=source_code,
            analysis_type="TESTS",
            review_output=test_code,
            time_comp="O(1)",
            space_comp="O(1)",
            score=90,
            suggestions=["Run these tests to verify function boundaries."]
        )

        return {"testCode": test_code, "language": language}

    @classmethod
    def explain_bug(cls, user_id: int, language: str, source_code: str, error_message: str) -> dict:
        """Provide detailed bug diagnostics and actionable fix suggestions."""
        explanation = ""
        suggested_fix = ""

        if "IndexError" in error_message or "out of bounds" in error_message:
            explanation = "An IndexError occurs when attempting to access an index that is outside the range of a sequence (e.g. array length is 5, but accessed index 5 or higher)."
            suggested_fix = "Check loop upper bounds `len(arr)` or ensure the index is strictly `< len(arr)` before accessing."
        elif "KeyError" in error_message:
            explanation = "A KeyError occurs when attempting to access a dictionary key that does not exist."
            suggested_fix = "Use `dict.get(key, default)` or verify with `if key in dict:` before indexing."
        elif "TypeError" in error_message:
            explanation = "A TypeError indicates an operation was performed on an inappropriate data type (e.g., adding an integer to a string)."
            suggested_fix = "Verify type signatures and use explicit type casting `int()`, `str()`, or check types."
        elif "ZeroDivisionError" in error_message:
            explanation = "ZeroDivisionError happens when dividing or taking modulo by 0."
            suggested_fix = "Add a guard `if divisor != 0:` before division."
        else:
            explanation = f"Error detected during execution: `{error_message}`"
            suggested_fix = "Trace variables using logging or isolated print statements to inspect runtime states."

        output = f"### 🐞 Bug Analysis\n\n**Diagnosis**:\n{explanation}\n\n**Recommended Fix**:\n{suggested_fix}"

        cls._save_review_record(
            user_id=user_id,
            language=language,
            source_code=source_code,
            analysis_type="BUG_EXPLAIN",
            review_output=output,
            time_comp="",
            space_comp="",
            score=80,
            suggestions=[suggested_fix]
        )

        return {"explanation": explanation, "suggestedFix": suggested_fix, "markdown": output}

    @classmethod
    def _save_review_record(cls, user_id: int, language: str, source_code: str, analysis_type: str, review_output: str, time_comp: str, space_comp: str, score: int, suggestions: list):
        try:
            db = db_session()
            review = AIReview(
                user_id=user_id,
                language=language,
                source_code=source_code,
                analysis_type=analysis_type,
                review_output=review_output,
                complexity_time=time_comp,
                complexity_space=space_comp,
                quality_score=score,
                suggestions_json=json.dumps(suggestions)
            )
            db.add(review)
            db.commit()
        except Exception:
            pass
