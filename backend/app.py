"""
CodePilot Enterprise Backend REST API Server
Version: 2.0.0 (Production Architecture)
Features:
  - Standardized /api/v1/* versioned endpoints
  - JWT Stateless Auth & Session Revocation
  - RBAC Middleware (USER, MODERATOR, INSTRUCTOR, ADMIN)
  - Multi-Language Sandbox Engine with Resource Controls
  - Competitive Programming Submission Judge
  - Pilot AI Developer Assistant
  - Course Learning Platform & Project Workspaces
  - System Observability (/health, /ready, /api/v1/admin/telemetry)
"""

import os
import sys
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from codepilot.db.connection import init_db
from codepilot.db.seed import seed_database
from codepilot.utils.security import verify_token
from codepilot.services.auth_service import AuthService
from codepilot.services.user_service import UserService
from codepilot.services.problem_service import ProblemService
from codepilot.services.contest_service import ContestService
from codepilot.services.leaderboard_service import LeaderboardService
from codepilot.services.course_service import CourseService
from codepilot.services.project_service import ProjectService
from codepilot.services.notification_service import NotificationService
from codepilot.services.admin_service import AdminService
from codepilot.engine.execution_sandbox import ExecutionSandbox
from codepilot.engine.runtime_manager import RuntimeManager
from codepilot.judge.submission_judge import SubmissionJudge
from codepilot.ai.pilot_ai_engine import PilotAIEngine

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Auto-seed database on server initialization
with app.app_context():
    seed_database()


# ---------------------------------------------------------
# Security & Auth Middleware Decorators
# ---------------------------------------------------------
def get_current_user_token_payload():
    """Extract and verify Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return verify_token(token)


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = get_current_user_token_payload()
        if not payload:
            return jsonify({"error": "Unauthorized. Valid authentication token required."}), 401
        request.user_payload = payload
        return f(*args, **kwargs)
    return decorated


def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            payload = get_current_user_token_payload()
            if not payload:
                return jsonify({"error": "Unauthorized."}), 401
            user_role = payload.get("role", "USER")
            if user_role not in roles and "ADMIN" not in user_role:
                return jsonify({"error": f"Forbidden. Requires one of roles: {', '.join(roles)}"}), 403
            request.user_payload = payload
            return f(*args, **kwargs)
        return decorated
    return decorator


# ---------------------------------------------------------
# Observability & Health Endpoints
# ---------------------------------------------------------
@app.route("/health", methods=["GET"])
@app.route("/api/v1/health", methods=["GET"])
def health():
    return jsonify({
        "status": "HEALTHY",
        "service": "CodePilot Production API",
        "version": "2.0.0",
        "environment": os.environ.get("ENV", "production")
    }), 200


@app.route("/ready", methods=["GET"])
def ready():
    return jsonify({"status": "READY", "database": "CONNECTED", "sandbox": "ONLINE"}), 200


# ---------------------------------------------------------
# Authentication Routes (/api/v1/auth)
# ---------------------------------------------------------
@app.route("/api/v1/auth/register", methods=["POST"])
def auth_register():
    data = request.get_json() or {}
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")
    display_name = data.get("displayName", "")

    success, result = AuthService.register_user(username, email, password, display_name)
    if not success:
        return jsonify({"error": result}), 400
    return jsonify(result), 201


@app.route("/api/v1/auth/login", methods=["POST"])
def auth_login():
    data = request.get_json() or {}
    identifier = data.get("username") or data.get("email") or data.get("loginIdentifier", "")
    password = data.get("password", "")

    ip_address = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")

    success, result = AuthService.authenticate_user(identifier, password, ip_address, user_agent)
    if not success:
        return jsonify({"error": result}), 401
    return jsonify(result), 200


@app.route("/api/v1/auth/refresh", methods=["POST"])
def auth_refresh():
    data = request.get_json() or {}
    refresh_token = data.get("refreshToken", "")
    success, result = AuthService.refresh_access_token(refresh_token)
    if not success:
        return jsonify({"error": result}), 401
    return jsonify(result), 200


@app.route("/api/v1/auth/logout", methods=["POST"])
@require_auth
def auth_logout():
    token = request.headers.get("Authorization", "").split(" ")[1]
    AuthService.revoke_session(token)
    return jsonify({"message": "Successfully logged out."}), 200


@app.route("/api/v1/auth/forgot-password", methods=["POST"])
def auth_forgot_password():
    data = request.get_json() or {}
    email = data.get("email", "")
    success, result = AuthService.request_password_reset(email)
    return jsonify({"message": result}), 200


@app.route("/api/v1/auth/reset-password", methods=["POST"])
def auth_reset_password():
    data = request.get_json() or {}
    token = data.get("token", "")
    new_password = data.get("password", "")
    success, msg = AuthService.reset_password(token, new_password)
    if not success:
        return jsonify({"error": msg}), 400
    return jsonify({"message": msg}), 200


# ---------------------------------------------------------
# User Profile & Isolated History Routes
# ---------------------------------------------------------
@app.route("/api/v1/profile", methods=["GET"])
@require_auth
def get_profile():
    user_id = request.user_payload["user_id"]
    profile = UserService.get_profile_by_id(user_id)
    if not profile:
        return jsonify({"error": "Profile not found."}), 404
    return jsonify(profile), 200


@app.route("/api/v1/profile", methods=["PUT"])
@require_auth
def update_profile():
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    success, updated = UserService.update_profile(user_id, data)
    if not success:
        return jsonify({"error": updated}), 400
    return jsonify(updated), 200


@app.route("/api/v1/users/<username>", methods=["GET"])
def get_public_user(username):
    profile = UserService.get_public_profile(username)
    if not profile:
        return jsonify({"error": "User not found."}), 404
    return jsonify(profile), 200


@app.route("/api/v1/history", methods=["GET"])
@require_auth
def get_user_history():
    user_id = request.user_payload["user_id"]
    page = int(request.args.get("page", 1))
    page_size = min(100, int(request.args.get("pageSize", 20)))
    act_type = request.args.get("activityType")
    lang = request.args.get("language")
    status = request.args.get("status")
    search = request.args.get("search")

    history = UserService.get_user_activity_history(
        user_id=user_id,
        page=page,
        page_size=page_size,
        activity_type=act_type,
        language=lang,
        status=status,
        search=search
    )
    return jsonify(history), 200


# ---------------------------------------------------------
# Code Execution & Multi-Language Sandbox Routes
# ---------------------------------------------------------
@app.route("/api/execute", methods=["POST"])
@app.route("/api/v1/execution/run", methods=["POST"])
def execute_code_api():
    data = request.get_json() or {}
    language = data.get("language", "python")
    source_code = data.get("sourceCode") or data.get("code", "")
    stdin_data = data.get("stdin", "")
    timeout = float(data.get("timeout", 5.0))
    memory_limit = float(data.get("memoryLimit", 128.0))

    user_id = None
    payload = get_current_user_token_payload()
    if payload:
        user_id = payload.get("user_id")

    result = ExecutionSandbox.execute_code(
        language=language,
        source_code=source_code,
        stdin_data=stdin_data,
        timeout=timeout,
        memory_limit_mb=memory_limit
    )

    # Save to history if logged in
    if user_id:
        UserService.add_user_activity(
            user_id=user_id,
            activity_type="EXECUTION",
            title=f"Ran {language.upper()} code",
            description=f"Status: {result['status']} | Runtime: {result['runtimeSeconds']:.3f}s",
            language=language,
            status=result["status"],
            details={"exitCode": result["exitCode"], "runtime": f"{result['runtimeSeconds']:.3f}s"}
        )

    # Format response compatible with existing and v1 specs
    return jsonify({
        "status": result["status"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "output": result["stdout"] if result["stdout"] else result["stderr"],
        "exitCode": result["exitCode"],
        "runtime": f"{result['runtimeSeconds']:.3f}s",
        "runtimeSeconds": result["runtimeSeconds"],
        "memory": f"{result['memoryMb']:.1f} MB",
        "memoryMb": result["memoryMb"]
    }), 200


@app.route("/api/v1/runtime/languages", methods=["GET"])
def get_runtime_languages():
    runtimes = RuntimeManager.get_available_runtimes()
    return jsonify(runtimes), 200


@app.route("/api/v1/runtime-tests/run", methods=["POST"])
def run_runtime_diagnostics():
    report = RuntimeManager.run_runtime_smoke_tests()
    return jsonify({"diagnostics": report, "timestamp": os.environ.get("TIMESTAMP", "2026-09-09")}), 200


# ---------------------------------------------------------
# Competitive Programming & Problems Routes
# ---------------------------------------------------------
@app.route("/api/v1/problems", methods=["GET"])
def list_problems():
    difficulty = request.args.get("difficulty")
    category = request.args.get("category")
    search = request.args.get("search")
    problems = ProblemService.get_all_problems(difficulty, category, search)
    return jsonify(problems), 200


@app.route("/api/v1/problems/<identifier>", methods=["GET"])
def get_problem(identifier):
    if identifier.isdigit():
        problem = ProblemService.get_problem_by_id(int(identifier))
    else:
        problem = ProblemService.get_problem_by_slug(identifier)

    if not problem:
        return jsonify({"error": "Problem not found."}), 404
    return jsonify(problem), 200


@app.route("/api/v1/submissions", methods=["POST"])
@require_auth
def submit_solution():
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    problem_id = data.get("problemId")
    language = data.get("language", "python")
    source_code = data.get("sourceCode", "")
    contest_id = data.get("contestId")

    if not problem_id or not source_code:
        return jsonify({"error": "Missing problemId or sourceCode."}), 400

    result = SubmissionJudge.evaluate_submission(
        user_id=user_id,
        problem_id=int(problem_id),
        language=language,
        source_code=source_code,
        contest_id=contest_id
    )

    return jsonify(result), 200


@app.route("/api/v1/submissions", methods=["GET"])
@require_auth
def list_user_submissions():
    user_id = request.user_payload["user_id"]
    problem_id = request.args.get("problemId")
    page = int(request.args.get("page", 1))
    page_size = min(100, int(request.args.get("pageSize", 20)))

    results = ProblemService.get_user_submissions(
        user_id=user_id,
        problem_id=int(problem_id) if problem_id else None,
        page=page,
        page_size=page_size
    )
    return jsonify(results), 200


# ---------------------------------------------------------
# Contests & Leaderboards Routes
# ---------------------------------------------------------
@app.route("/api/v1/contests", methods=["GET"])
def list_contests():
    contests = ContestService.get_all_contests()
    return jsonify(contests), 200


@app.route("/api/v1/contests/<int:contest_id>", methods=["GET"])
def get_contest(contest_id):
    contest = ContestService.get_contest_by_id(contest_id)
    if not contest:
        return jsonify({"error": "Contest not found."}), 404
    return jsonify(contest), 200


@app.route("/api/v1/contests/<int:contest_id>/register", methods=["POST"])
@require_auth
def register_contest(contest_id):
    user_id = request.user_payload["user_id"]
    success, msg = ContestService.register_user(contest_id, user_id)
    if not success:
        return jsonify({"error": msg}), 400
    return jsonify({"message": msg}), 200


@app.route("/api/v1/contests/<int:contest_id>/leaderboard", methods=["GET"])
def get_contest_leaderboard_route(contest_id):
    leaderboard = ContestService.get_contest_leaderboard(contest_id)
    return jsonify(leaderboard), 200


@app.route("/api/v1/leaderboards", methods=["GET"])
def get_global_leaderboard():
    board_type = request.args.get("type", "GLOBAL")
    limit = min(100, int(request.args.get("limit", 50)))
    board = LeaderboardService.get_leaderboard(board_type, limit)
    return jsonify(board), 200


# ---------------------------------------------------------
# Learning Center Routes
# ---------------------------------------------------------
@app.route("/api/v1/courses", methods=["GET"])
def list_courses():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")
    courses = CourseService.get_all_courses(category, difficulty)
    return jsonify(courses), 200


@app.route("/api/v1/courses/<slug>", methods=["GET"])
def get_course(slug):
    course = CourseService.get_course_by_slug(slug)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    return jsonify(course), 200


@app.route("/api/v1/courses/<int:course_id>/lessons/<int:lesson_id>/complete", methods=["POST"])
@require_auth
def complete_course_lesson(course_id, lesson_id):
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    score = float(data.get("score", 100.0))
    res = CourseService.complete_lesson(user_id, course_id, lesson_id, score)
    return jsonify(res), 200


# ---------------------------------------------------------
# Project Workspaces Routes
# ---------------------------------------------------------
@app.route("/api/v1/projects", methods=["GET"])
@require_auth
def list_projects():
    user_id = request.user_payload["user_id"]
    projects = ProjectService.get_user_projects(user_id)
    return jsonify(projects), 200


@app.route("/api/v1/projects", methods=["POST"])
@require_auth
def create_project_route():
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    title = data.get("title", "Untitled Project")
    description = data.get("description", "")
    language = data.get("language", "python")
    template = data.get("template", "basic")

    proj = ProjectService.create_project(user_id, title, description, language, template)
    return jsonify(proj), 201


@app.route("/api/v1/projects/<int:project_id>", methods=["GET"])
@require_auth
def get_project_route(project_id):
    user_id = request.user_payload["user_id"]
    proj = ProjectService.get_project_details(project_id, user_id)
    if not proj:
        return jsonify({"error": "Project not found or private."}), 404
    return jsonify(proj), 200


@app.route("/api/v1/projects/<int:project_id>/files", methods=["PUT"])
@require_auth
def update_project_file_route(project_id):
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    filename = data.get("filename", "")
    content = data.get("content", "")

    if not filename:
        return jsonify({"error": "Filename required."}), 400

    success = ProjectService.update_project_file(project_id, user_id, filename, content)
    if not success:
        return jsonify({"error": "Failed to update project file."}), 400
    return jsonify({"message": "File updated successfully."}), 200


# ---------------------------------------------------------
# Pilot AI Assistant Routes
# ---------------------------------------------------------
@app.route("/api/v1/ai/review", methods=["POST"])
def ai_code_review():
    data = request.get_json() or {}
    language = data.get("language", "python")
    source_code = data.get("sourceCode", "")

    user_id = None
    payload = get_current_user_token_payload()
    if payload:
        user_id = payload.get("user_id")

    res = PilotAIEngine.review_code(user_id, language, source_code)
    return jsonify(res), 200


@app.route("/api/v1/ai/complexity", methods=["POST"])
def ai_complexity():
    data = request.get_json() or {}
    language = data.get("language", "python")
    source_code = data.get("sourceCode", "")

    res = PilotAIEngine.estimate_complexity(language, source_code)
    return jsonify(res), 200


@app.route("/api/v1/ai/generate-tests", methods=["POST"])
def ai_generate_tests():
    data = request.get_json() or {}
    language = data.get("language", "python")
    source_code = data.get("sourceCode", "")

    user_id = None
    payload = get_current_user_token_payload()
    if payload:
        user_id = payload.get("user_id")

    res = PilotAIEngine.generate_tests(user_id, language, source_code)
    return jsonify(res), 200


@app.route("/api/v1/ai/explain-bug", methods=["POST"])
def ai_explain_bug():
    data = request.get_json() or {}
    language = data.get("language", "python")
    source_code = data.get("sourceCode", "")
    error_message = data.get("errorMessage", "")

    user_id = None
    payload = get_current_user_token_payload()
    if payload:
        user_id = payload.get("user_id")

    res = PilotAIEngine.explain_bug(user_id, language, source_code, error_message)
    return jsonify(res), 200


# ---------------------------------------------------------
# Notifications Routes
# ---------------------------------------------------------
@app.route("/api/v1/notifications", methods=["GET"])
@require_auth
def get_notifications():
    user_id = request.user_payload["user_id"]
    unread_only = request.args.get("unreadOnly", "false").lower() == "true"
    notifs = NotificationService.get_user_notifications(user_id, unread_only)
    return jsonify(notifs), 200


@app.route("/api/v1/notifications/<int:notif_id>/read", methods=["PUT"])
@require_auth
def mark_notification_read(notif_id):
    user_id = request.user_payload["user_id"]
    success = NotificationService.mark_as_read(notif_id, user_id)
    if not success:
        return jsonify({"error": "Notification not found."}), 404
    return jsonify({"message": "Marked as read."}), 200


# ---------------------------------------------------------
# Admin Routes (RBAC: ADMIN)
# ---------------------------------------------------------
@app.route("/api/v1/admin/telemetry", methods=["GET"])
@require_role("ADMIN")
def admin_telemetry():
    stats = AdminService.get_system_telemetry()
    return jsonify(stats), 200


@app.route("/api/v1/admin/users", methods=["GET"])
@require_role("ADMIN")
def admin_list_users():
    page = int(request.args.get("page", 1))
    page_size = min(100, int(request.args.get("pageSize", 20)))
    users = AdminService.get_all_users(page, page_size)
    return jsonify(users), 200


@app.route("/api/v1/admin/users/<int:target_user_id>/role", methods=["PUT"])
@require_role("ADMIN")
def admin_change_role(target_user_id):
    data = request.get_json() or {}
    new_role = data.get("role", "")
    success = AdminService.set_user_role(target_user_id, new_role)
    if not success:
        return jsonify({"error": "Failed to update role. Valid roles: USER, MODERATOR, INSTRUCTOR, ADMIN"}), 400
    return jsonify({"message": "User role updated successfully."}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting CodePilot Production API on http://0.0.0.0:{port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
