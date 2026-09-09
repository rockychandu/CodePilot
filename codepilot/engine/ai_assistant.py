"""
CodePilot AI Assistant Engine in Python
"""

from codepilot.engine.sandbox import PythonEngine

class PilotAIEngine:
    @staticmethod
    def generate_review(source_code: str) -> dict:
        analysis = PythonEngine.analyze_code(source_code)

        if not analysis.get("valid"):
            return {
                "score": 30,
                "summary": "Code contains syntax errors.",
                "issues": [analysis.get("error")],
                "recommendations": ["Fix syntax error before running AI code review."]
            }

        issues = []
        recommendations = []

        if analysis.get("loops") >= 2:
            issues.append("Nested loops detected. Potential O(N^2) complexity performance bottleneck.")
            recommendations.append("Consider replacing nested loops with a Python dictionary / Hash Map.")

        if not analysis.get("functions"):
            recommendations.append("Wrap your code inside modular Python functions for reusability.")

        score = max(50, 100 - (len(issues) * 20))

        return {
            "score": score,
            "complexity": analysis.get("complexity"),
            "summary": f"Code analysis complete. Score: {score}/100.",
            "issues": issues if issues else ["No critical issues detected."],
            "recommendations": recommendations if recommendations else ["Code follows standard Python conventions."]
        }

    @staticmethod
    def explain_code(source_code: str, topic: str = "general") -> str:
        analysis = PythonEngine.analyze_code(source_code)
        return (
            f"### Pilot AI Explanation\n\n"
            f"**Overview:** This code uses Python constructs with estimated time complexity {analysis.get('complexity', 'O(N)')}.\n"
            f"**Structure:** Contains {analysis.get('functions', 0)} function(s) and {analysis.get('loops', 0)} loop(s).\n"
            f"**Imports:** {', '.join(analysis.get('imports', [])) if analysis.get('imports') else 'None'}"
        )
