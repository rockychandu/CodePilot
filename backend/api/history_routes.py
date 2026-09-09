"""
User Profile & History API Blueprint (/api/v1/profile, /api/v1/users, /api/v1/history)
"""

from flask import Blueprint, request, jsonify
from backend.users.user_service import UserService
from backend.history.history_service import HistoryService
from backend.middleware.auth_middleware import require_auth

history_bp = Blueprint("history_bp", __name__, url_prefix="/api/v1")

@history_bp.route("/profile", methods=["GET"])
@require_auth
def get_current_profile():
    uid = request.user_payload["user_id"]
    prof = UserService.get_profile_by_id(uid)
    if not prof:
        return jsonify({"error": "Profile not found."}), 404
    return jsonify(prof), 200

@history_bp.route("/profile", methods=["PUT"])
@require_auth
def update_current_profile():
    uid = request.user_payload["user_id"]
    data = request.get_json() or {}
    success, updated = UserService.update_profile(uid, data)
    if not success:
        return jsonify({"error": updated}), 400
    return jsonify(updated), 200

@history_bp.route("/users/<username>", methods=["GET"])
def get_user_public(username):
    prof = UserService.get_public_profile(username)
    if not prof:
        return jsonify({"error": "User not found."}), 404
    return jsonify(prof), 200

@history_bp.route("/history", methods=["GET"])
@require_auth
def get_history():
    uid = request.user_payload["user_id"]
    page = int(request.args.get("page", 1))
    page_size = min(100, int(request.args.get("pageSize", 20)))
    act_type = request.args.get("activityType")
    lang = request.args.get("language")
    status = request.args.get("status")
    search = request.args.get("search")

    return jsonify(HistoryService.get_history(
        user_id=uid,
        page=page,
        page_size=page_size,
        activity_type=act_type,
        language=lang,
        status=status,
        search=search
    )), 200

@history_bp.route("/history/<int:activity_id>", methods=["GET"])
@require_auth
def get_history_detail(activity_id):
    uid = request.user_payload["user_id"]
    detail = HistoryService.get_activity_detail(activity_id, uid)
    if not detail:
        return jsonify({"error": "Activity record not found."}), 404
    return jsonify(detail), 200
