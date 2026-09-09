"""
Competitive Programming Judge Engine
Executes test cases (public and hidden) sequentially, checks outputs, aggregates scores, and records submissions.
"""

import json
import time
from typing import Dict, Any, Optional
from backend.repositories.problem_repository import ProblemRepository
from backend.repositories.submission_repository import SubmissionRepository
from backend.repositories.user_repository import UserRepository
from backend.repositories.history_repository import HistoryRepository
from backend.repositories.notification_repository import NotificationRepository
from backend.execution.execution_engine import ExecutionEngine

class JudgeService:
    @staticmethod
    def evaluate(
        user_id: int,
        problem_id: int,
        language: str,
        source_code: str,
        contest_id: Optional[int] = None
    ) -> Dict[str, Any]:
        test_cases = ProblemRepository.get_test_cases_for_judge(problem_id)
        if not test_cases:
            return {
                "status": "ERROR",
                "message": "No test cases configured for this problem.",
                "passedTests": 0,
                "totalTests": 0
            }

        problem = ProblemRepository.get_by_id(problem_id)
        time_limit = problem.get("timeLimit", 2.0) if problem else 2.0
        memory_limit = problem.get("memoryLimit", 128.0) if problem else 128.0

        total_tests = len(test_cases)
        passed_tests = 0
        overall_status = "Accepted"
        total_runtime = 0.0
        max_memory = 0.0
        compiler_output = ""
        per_test_results = []

        for i, tc in enumerate(test_cases, 1):
            res = ExecutionEngine.run_code(
                language=language,
                source_code=source_code,
                stdin_data=tc.input_data,
                timeout=time_limit,
                memory_limit_mb=memory_limit,
                user_id=None  # Avoid duplicate activity log per test case
            )

            total_runtime += res["runtimeSeconds"]
            max_memory = max(max_memory, res["memoryMb"])

            if res["status"] == "COMPILE_ERROR":
                overall_status = "Compilation Error"
                compiler_output = res["stderr"]
                per_test_results.append({
                    "testIndex": i,
                    "status": "Compilation Error",
                    "isHidden": tc.is_hidden,
                    "runtime": f"{res['runtimeSeconds']:.3f}s"
                })
                break

            if res["status"] == "TIME_LIMIT_EXCEEDED":
                overall_status = "Time Limit Exceeded"
                per_test_results.append({
                    "testIndex": i,
                    "status": "Time Limit Exceeded",
                    "isHidden": tc.is_hidden,
                    "runtime": f"{res['runtimeSeconds']:.3f}s"
                })
                break

            if res["status"] == "RUNTIME_ERROR":
                overall_status = "Runtime Error"
                per_test_results.append({
                    "testIndex": i,
                    "status": "Runtime Error",
                    "isHidden": tc.is_hidden,
                    "runtime": f"{res['runtimeSeconds']:.3f}s",
                    "error": res["stderr"]
                })
                break

            # Compare output
            expected = tc.expected_output.strip().replace("\r\n", "\n")
            actual = res["stdout"].strip().replace("\r\n", "\n")

            if expected == actual:
                passed_tests += 1
                per_test_results.append({
                    "testIndex": i,
                    "status": "Passed",
                    "isHidden": tc.is_hidden,
                    "runtime": f"{res['runtimeSeconds']:.3f}s"
                })
            else:
                overall_status = "Wrong Answer"
                per_test_results.append({
                    "testIndex": i,
                    "status": "Wrong Answer",
                    "isHidden": tc.is_hidden,
                    "input": tc.input_data if not tc.is_hidden else "[Hidden]",
                    "expected": expected if not tc.is_hidden else "[Hidden]",
                    "actual": actual if not tc.is_hidden else "[Hidden]",
                    "runtime": f"{res['runtimeSeconds']:.3f}s"
                })
                break

        avg_runtime = total_runtime / max(1, len(per_test_results))

        # Record submission
        sub_dict = SubmissionRepository.create_submission(
            user_id=user_id,
            problem_id=problem_id,
            language=language,
            source_code=source_code,
            status=overall_status,
            passed_tests=passed_tests,
            total_tests=total_tests,
            runtime_seconds=avg_runtime,
            memory_mb=max_memory,
            compiler_output=compiler_output,
            test_results_json=json.dumps(per_test_results),
            contest_id=contest_id
        )

        # Update XP & Stats if Accepted
        if overall_status == "Accepted":
            UserRepository.update_stats(user_id=user_id, xp_gain=50, problems_solved_gain=1)
            NotificationRepository.create_notification(
                user_id=user_id,
                title="Problem Solved!",
                message=f"Congratulations! You solved '{problem['title'] if problem else 'Problem'}' (+50 XP).",
                category="SUBMISSION"
            )

        HistoryRepository.record_activity(
            user_id=user_id,
            activity_type="SUBMISSION",
            title=f"Submitted {problem['title'] if problem else 'Problem'}",
            description=f"Status: {overall_status} ({passed_tests}/{total_tests} tests passed)",
            language=language,
            status=overall_status,
            details={
                "submissionId": sub_dict["id"],
                "passed": passed_tests,
                "total": total_tests,
                "runtime": f"{avg_runtime:.3f}s"
            }
        )

        return {
            "submissionId": sub_dict["id"],
            "status": overall_status,
            "passedTests": passed_tests,
            "totalTests": total_tests,
            "runtime": f"{avg_runtime:.3f}s",
            "memory": f"{max_memory:.1f} MB",
            "compilerOutput": compiler_output,
            "testResults": per_test_results
        }
