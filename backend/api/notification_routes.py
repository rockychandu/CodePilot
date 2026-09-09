"""
Notifications API Blueprint (/api/v1/notifications)
"""

from flask import Blueprint, request, jsonify
from backend.notifications.notification_service import NotificationService
from backend.middleware.auth_middleware import require_auth

notification_bp = Blueprint("notification_bp", __name__, url_prefix="/api/v1/notifications")

@notification_bp.route("", methods=["GET"])
@require_auth
def get_notifications():
    uid = request.user_payload["user_id"]
    unread = request.args.get("unreadOnly", "false").lower() == "true"
    return jsonify(NotificationService.get_user_notifications(uid, unread_only=unread)), 200

@notification_bp.route("/<int:notification_id>/read", methods=["PUT"])
@require_auth
def mark_read(notification_id):
    uid = request.user_payload["user_id"]
    success = NotificationService.mark_as_read(notification_id, uid)
    if not success:
        return jsonify({"error": "Notification not found."}), 404
    return jsonify({"message": "Marked as read."}), 200
