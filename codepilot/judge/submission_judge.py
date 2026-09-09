"""
CodePilot Competitive Programming Submission Judge
Evaluates code submissions against public and hidden test cases, computes verdicts,
calculates runtime/memory metrics, and awards XP.
"""

import json
import time
from codepilot.db.connection import db_session
from codepilot.db.models import Problem, TestCase, Submission, User, Profile, ActivityHistory
from codepilot.engine.execution_sandbox import ExecutionSandbox
from codepilot.services.user_service import UserService


class SubmissionJudge:
    @classmethod
    def evaluate_submission(
        cls,
        user_id: int,
        problem_id: int,
        language: str,
        source_code: str,
        contest_id: int = None
    ) -> dict:
        """
        Run code against all test cases for the problem and persist the submission.
        """
        db = db_session()
        problem = db.query(Problem).filter_by(id=problem_id).first()
        if not problem:
            return {"status": "INTERNAL_ERROR", "message": "Problem not found."}

        test_cases = db.query(TestCase).filter_by(problem_id=problem_id).order_by(TestCase.order_index).all()
        if not test_cases:
            return {"status": "INTERNAL_ERROR", "message": "No test cases configured for problem."}

        total_tests = len(test_cases)
        passed_tests = 0
        overall_status = "Accepted"
        max_runtime = 0.0
        max_memory = 0.0
        compiler_output = ""
        test_results = []

        for idx, tc in enumerate(test_cases):
            res = ExecutionSandbox.execute_code(
                language=language,
                source_code=source_code,
                stdin_data=tc.input_data,
                timeout=problem.time_limit_seconds,
                memory_limit_mb=problem.memory_limit_mb
            )

            max_runtime = max(max_runtime, res.get("runtimeSeconds", 0.0))
            max_memory = max(max_memory, res.get("memoryMb", 0.0))

            if res["status"] == "COMPILE_ERROR":
                overall_status = "Compilation Error"
                compiler_output = res.get("stderr", "") or res.get("stdout", "")
                test_results.append({
                    "testCase": idx + 1,
                    "status": "Compilation Error",
                    "isHidden": tc.is_hidden,
                    "error": compiler_output
                })
                break

            elif res["status"] == "TIME_LIMIT_EXCEEDED":
                overall_status = "Time Limit Exceeded"
                test_results.append({
                    "testCase": idx + 1,
                    "status": "Time Limit Exceeded",
                    "isHidden": tc.is_hidden,
                    "runtime": f"{res.get('runtimeSeconds', 0.0):.3f}s"
                })
                break

            elif res["status"] == "RUNTIME_ERROR":
                overall_status = "Runtime Error"
                test_results.append({
                    "testCase": idx + 1,
                    "status": "Runtime Error",
                    "isHidden": tc.is_hidden,
                    "stderr": res.get("stderr", "")
                })
                break

            # Compare output
            actual = res.get("stdout", "").strip()
            expected = tc.expected_output.strip()

            # Normalize lines/whitespace
            is_match = (actual == expected) or (actual.replace("\r\n", "\n") == expected.replace("\r\n", "\n"))

            if is_match:
                passed_tests += 1
                test_results.append({
                    "testCase": idx + 1,
                    "status": "Passed",
                    "isHidden": tc.is_hidden,
                    "runtime": f"{res.get('runtimeSeconds', 0.0):.3f}s"
                })
            else:
                overall_status = "Wrong Answer"
                test_results.append({
                    "testCase": idx + 1,
                    "status": "Wrong Answer",
                    "isHidden": tc.is_hidden,
                    "input": tc.input_data if not tc.is_hidden else "(Hidden Test Case)",
                    "expected": expected if not tc.is_hidden else "(Hidden)",
                    "actual": actual if not tc.is_hidden else "(Hidden)",
                    "runtime": f"{res.get('runtimeSeconds', 0.0):.3f}s"
                })
                break

        # Save submission record
        submission = Submission(
            user_id=user_id,
            problem_id=problem_id,
            contest_id=contest_id,
            language=language,
            source_code=source_code,
            status=overall_status,
            passed_tests=passed_tests,
            total_tests=total_tests,
            runtime_seconds=max_runtime,
            memory_mb=max_memory,
            compiler_output=compiler_output,
            test_results_json=json.dumps(test_results)
        )
        db.add(submission)

        # Update problem statistics
        problem.total_submissions += 1
        if overall_status == "Accepted":
            problem.accepted_submissions += 1

            # Update User profile stats & award XP
            user = db.query(User).filter_by(id=user_id).first()
            if user and user.profile:
                # Check if this user solved this problem previously
                prev_accepted = db.query(Submission).filter_by(
                    user_id=user_id, problem_id=problem_id, status="Accepted"
                ).first()
                if not prev_accepted:
                    user.profile.problems_solved += 1
                    # Easy: 50 XP, Medium: 100 XP, Hard: 200 XP
                    xp_gain = 50 if problem.difficulty == "Easy" else (100 if problem.difficulty == "Medium" else 200)
                    UserService.award_xp(user_id, xp_gain)

        # Record activity
        UserService.add_user_activity(
            user_id=user_id,
            activity_type="SUBMISSION",
            title=f"Submitted to {problem.title}",
            description=f"Verdict: {overall_status} ({passed_tests}/{total_tests} tests passed)",
            language=language,
            status=overall_status,
            details={"problemId": problem_id, "submissionId": submission.id, "runtime": f"{max_runtime:.3f}s"}
        )

        db.commit()

        return {
            "id": submission.id,
            "problemId": problem_id,
            "problemTitle": problem.title,
            "status": overall_status,
            "passedTests": passed_tests,
            "totalTests": total_tests,
            "runtime": f"{max_runtime:.3f}s",
            "memory": f"{max_memory:.1f} MB",
            "compilerOutput": compiler_output,
            "testResults": test_results
        }
