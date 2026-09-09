"""
Centralized Error Handlers for API Exception Management
"""

import traceback
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"success": False, "error": "Bad Request", "details": str(e)}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"success": False, "error": "Unauthorized", "details": str(e)}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"success": False, "error": "Forbidden", "details": str(e)}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Resource Not Found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "error": "Method Not Allowed"}), 405

    @app.errorhandler(429)
    def too_many_requests(e):
        return jsonify({"success": False, "error": "Too Many Requests"}), 429

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server."
        }), 500
