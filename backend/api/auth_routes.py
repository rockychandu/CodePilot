"""
Auth API Blueprint (/api/v1/auth)
Provides complete enterprise authentication endpoints.
"""

from flask import Blueprint, request, jsonify
from backend.auth.service import AuthService
from backend.middleware.auth_middleware import require_auth
from backend.middleware.rate_limit_middleware import limit_requests

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1/auth")

@auth_bp.route("/register", methods=["POST"])
@limit_requests(max_per_minute=20)
def register():
    data = request.get_json() or {}
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")
    confirm_password = data.get("confirmPassword") or data.get("confirm_password")
    display_name = data.get("displayName") or data.get("display_name", "")
    ip = request.remote_addr

    success, result = AuthService.register_user(
        username=username,
        email=email,
        password=password,
        confirm_password=confirm_password,
        display_name=display_name,
        ip_address=ip
    )
    if not success:
        return jsonify({"success": False, "error": result}), 400
    return jsonify({"success": True, **result}), 201

@auth_bp.route("/login", methods=["POST"])
@limit_requests(max_per_minute=30)
def login():
    data = request.get_json() or {}
    identifier = data.get("username") or data.get("email") or data.get("loginIdentifier") or data.get("identifier", "")
    password = data.get("password", "")
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "")

    success, result = AuthService.authenticate_user(identifier, password, ip, ua)
    if not success:
        return jsonify({"success": False, "error": result}), 401
    return jsonify({"success": True, **result}), 200

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json() or {}
    ref_tok = data.get("refreshToken") or data.get("refresh_token", "")
    success, result = AuthService.refresh_access_token(ref_tok)
    if not success:
        return jsonify({"success": False, "error": result}), 401
    return jsonify({"success": True, **result}), 200

@auth_bp.route("/me", methods=["GET"])
@require_auth
def get_current_user():
    payload = request.user_payload
    user_id = payload.get("user_id")
    user_data = AuthService.get_me(user_id)
    if not user_data:
        return jsonify({"success": False, "error": "User not found or inactive."}), 404
    return jsonify({"success": True, "user": user_data}), 200

@auth_bp.route("/logout", methods=["POST"])
@require_auth
def logout():
    auth_h = request.headers.get("Authorization", "")
    if auth_h.startswith("Bearer "):
        AuthService.revoke_session(auth_h[7:].strip())
    return jsonify({"success": True, "message": "Logged out successfully."}), 200

@auth_bp.route("/logout-all", methods=["POST"])
@require_auth
def logout_all():
    payload = request.user_payload
    user_id = payload.get("user_id")
    count = AuthService.revoke_all_sessions(user_id)
    return jsonify({"success": True, "message": f"Revoked {count} active sessions."}), 200

@auth_bp.route("/change-password", methods=["PUT", "POST"])
@require_auth
def change_password():
    payload = request.user_payload
    user_id = payload.get("user_id")
    data = request.get_json() or {}
    current_password = data.get("currentPassword") or data.get("current_password", "")
    new_password = data.get("newPassword") or data.get("new_password", "")

    success, msg = AuthService.change_password(user_id, current_password, new_password)
    if not success:
        return jsonify({"success": False, "error": msg}), 400
    return jsonify({"success": True, "message": msg}), 200

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json() or {}
    email = data.get("email", "")
    success, msg = AuthService.request_password_reset(email)
    return jsonify({"success": True, "message": msg}), 200

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    token = data.get("token", "")
    new_pwd = data.get("password") or data.get("newPassword", "")
    success, msg = AuthService.reset_password(token, new_pwd)
    if not success:
        return jsonify({"success": False, "error": msg}), 400
    return jsonify({"success": True, "message": msg}), 200

@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.get_json() or {}
    token = data.get("token", "")
    success, msg = AuthService.verify_email(token)
    if not success:
        return jsonify({"success": False, "error": msg}), 400
    return jsonify({"success": True, "message": msg}), 200

@auth_bp.route("/resend-verification", methods=["POST"])
def resend_verification():
    data = request.get_json() or {}
    email = data.get("email", "")
    success, msg = AuthService.resend_verification(email)
    return jsonify({"success": True, "message": msg}), 200
