"""
CodePilot Python CLI Tool
Command line interface for CodePilot platform.
Run via: python -m codepilot [command]
"""

import sys
import argparse
from codepilot.engine.sandbox import PythonEngine
from codepilot.engine.ai_assistant import PilotAIEngine
from codepilot.services.problem_service import ProblemServicePython

def main():
    parser = argparse.ArgumentParser(description="CodePilot Python Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run and analyze a Python script")
    run_parser.add_argument("file", help="Path to Python file")

    # Command: review
    review_parser = subparsers.add_parser("review", help="Run AI code review on Python file")
    review_parser.add_argument("file", help="Path to Python file")

    # Command: list
    subparsers.add_parser("list", help="List available coding problems")

    args = parser.parse_args()

    if args.command == "run":
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()
            res = PythonEngine.run_simulated(code)
            print(f"Status: {res['status']}")
            print(f"Runtime: {res['runtime']}")
            print(f"Output:\n{res['output']}")
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")

    elif args.command == "review":
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()
            review = PilotAIEngine.generate_review(code)
            print(f"=== Pilot AI Code Review ===")
            print(f"Score: {review['score']}/100")
            print(f"Complexity: {review['complexity']}")
            print(f"Summary: {review['summary']}")
            print(f"Recommendations: {', '.join(review['recommendations'])}")
        except Exception as e:
            print(f"Error reviewing file {args.file}: {e}")

    elif args.command == "list":
        svc = ProblemServicePython()
        problems = svc.get_all()
        print("=== CodePilot Problems List ===")
        for p in problems:
            print(f"[{p.id}] {p.title} ({p.difficulty.value}) - Solved: {p.solved_count}")

    else:
        print("CodePilot Python CLI v2.4.0 ('Code. Learn. Build. Compete.')")
        print("Usage: python -m codepilot [run | review | list]")

if __name__ == "__main__":
    main()
