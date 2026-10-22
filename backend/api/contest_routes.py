"""
Contest & Leaderboard API Blueprint (/api/v1/contests & /api/v1/leaderboards)
"""

from flask import Blueprint, request, jsonify
from backend.contests.contest_service import ContestService
from backend.leaderboards.leaderboard_service import LeaderboardService
from backend.middleware.auth_middleware import require_auth

contest_bp = Blueprint("contest_bp", __name__, url_prefix="/api/v1")

@contest_bp.route("/contests", methods=["GET"])
def list_contests():
    return jsonify(ContestService.get_all_contests()), 200

@contest_bp.route("/contests/<int:contest_id>", methods=["GET"])
def get_contest(contest_id):
    c = ContestService.get_contest_by_id(contest_id)
    if not c:
        return jsonify({"error": "Contest not found."}), 404
    return jsonify(c), 200

@contest_bp.route("/contests/<int:contest_id>/register", methods=["POST"])
@require_auth
def register_contest(contest_id):
    user_id = request.user_payload["user_id"]
    success, msg = ContestService.register_user(contest_id, user_id)
    if not success:
        return jsonify({"error": msg}), 400
    return jsonify({"message": msg}), 200

@contest_bp.route("/contests/<int:contest_id>/leaderboard", methods=["GET"])
def get_contest_leaderboard(contest_id):
    return jsonify(ContestService.get_contest_leaderboard(contest_id)), 200

@contest_bp.route("/leaderboards", methods=["GET"])
def get_global_leaderboard():
    btype = request.args.get("type", "GLOBAL")
    limit = min(100, int(request.args.get("limit", 50)))
    data = LeaderboardService.get_leaderboard(btype, limit)
    return jsonify(data.get("rankings", []) if isinstance(data, dict) else data), 200
