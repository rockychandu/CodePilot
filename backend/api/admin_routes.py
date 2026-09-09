"""
System Administration API Blueprint (/api/v1/admin)
"""

from flask import Blueprint, request, jsonify
from backend.admin.admin_service import AdminService
from backend.middleware.auth_middleware import require_role

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/v1/admin")

@admin_bp.route("/telemetry", methods=["GET"])
@require_role("ADMIN")
def telemetry():
    return jsonify(AdminService.get_system_telemetry()), 200

@admin_bp.route("/users", methods=["GET"])
@require_role("ADMIN")
def list_users():
    page = int(request.args.get("page", 1))
    page_size = min(100, int(request.args.get("pageSize", 20)))
    return jsonify(AdminService.get_all_users(page, page_size)), 200

@admin_bp.route("/users/<int:target_user_id>/role", methods=["PUT"])
@require_role("ADMIN")
def change_role(target_user_id):
    data = request.get_json() or {}
    new_role = data.get("role", "")
    success = AdminService.set_user_role(target_user_id, new_role)
    if not success:
        return jsonify({"error": "Failed to update role. Valid roles: USER, MODERATOR, INSTRUCTOR, ADMIN"}), 400
    return jsonify({"message": "Role updated successfully."}), 200
