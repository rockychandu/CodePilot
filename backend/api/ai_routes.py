"""
Pilot AI Assistant API Blueprint (/api/v1/ai)
"""

from flask import Blueprint, request, jsonify
from backend.ai.ai_service import AIService
from backend.middleware.auth_middleware import authenticate_request

ai_bp = Blueprint("ai_bp", __name__, url_prefix="/api/v1/ai")

@ai_bp.route("/review", methods=["POST"])
def review():
    data = request.get_json() or {}
    lang = data.get("language", "python")
    code = data.get("sourceCode", "")
    payload = authenticate_request()
    uid = payload.get("user_id") if payload else None

    return jsonify(AIService.review_code(uid, lang, code)), 200

@ai_bp.route("/complexity", methods=["POST"])
def complexity():
    data = request.get_json() or {}
    lang = data.get("language", "python")
    code = data.get("sourceCode", "")
    return jsonify(AIService.estimate_complexity(lang, code)), 200

@ai_bp.route("/generate-tests", methods=["POST"])
def generate_tests():
    data = request.get_json() or {}
    lang = data.get("language", "python")
    code = data.get("sourceCode", "")
    payload = authenticate_request()
    uid = payload.get("user_id") if payload else None

    return jsonify(AIService.generate_tests(uid, lang, code)), 200

@ai_bp.route("/explain-bug", methods=["POST"])
def explain_bug():
    data = request.get_json() or {}
    lang = data.get("language", "python")
    code = data.get("sourceCode", "")
    err = data.get("errorMessage", "")
    payload = authenticate_request()
    uid = payload.get("user_id") if payload else None

    return jsonify(AIService.explain_bug(uid, lang, code, err)), 200
