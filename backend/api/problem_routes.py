"""
Problem & Submission API Blueprint (/api/v1/problems & /api/v1/submissions)
"""

from flask import Blueprint, request, jsonify
from backend.problems.problem_service import ProblemService
from backend.submissions.judge_service import JudgeService
from backend.repositories.submission_repository import SubmissionRepository
from backend.middleware.auth_middleware import require_auth

problem_bp = Blueprint("problem_bp", __name__, url_prefix="/api/v1")

@problem_bp.route("/problems", methods=["GET"])
def get_problems():
    diff = request.args.get("difficulty")
    cat = request.args.get("category")
    q = request.args.get("search")
    problems = ProblemService.get_all_problems(difficulty=diff, category=cat, search=q)
    return jsonify(problems), 200

@problem_bp.route("/problems/<identifier>", methods=["GET"])
def get_problem_detail(identifier):
    if identifier.isdigit():
        p = ProblemService.get_problem_by_id(int(identifier))
    else:
        p = ProblemService.get_problem_by_slug(identifier)

    if not p:
        return jsonify({"error": "Problem not found."}), 404
    return jsonify(p), 200

@problem_bp.route("/submissions", methods=["POST"])
@require_auth
def submit():
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    problem_id = data.get("problemId")
    language = data.get("language", "python")
    source_code = data.get("sourceCode", "")
    contest_id = data.get("contestId")

    if not problem_id or not source_code:
        return jsonify({"error": "problemId and sourceCode are required."}), 400

    result = JudgeService.evaluate(
        user_id=user_id,
        problem_id=int(problem_id),
        language=language,
        source_code=source_code,
        contest_id=contest_id
    )
    return jsonify(result), 200

@problem_bp.route("/submissions", methods=["GET"])
@require_auth
def list_submissions():
    user_id = request.user_payload["user_id"]
    problem_id = request.args.get("problemId")
    page = int(request.args.get("page", 1))
    page_size = min(100, int(request.args.get("pageSize", 20)))

    results = SubmissionRepository.get_user_submissions(
        user_id=user_id,
        problem_id=int(problem_id) if problem_id else None,
        page=page,
        page_size=page_size
    )
    return jsonify(results), 200
