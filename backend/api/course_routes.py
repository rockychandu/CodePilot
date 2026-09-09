"""
Course & Learning API Blueprint (/api/v1/courses & /api/v1/learning)
"""

from flask import Blueprint, request, jsonify
from backend.courses.course_service import CourseService
from backend.learning.learning_service import LearningService
from backend.middleware.auth_middleware import require_auth, authenticate_request

course_bp = Blueprint("course_bp", __name__, url_prefix="/api/v1")

@course_bp.route("/courses", methods=["GET"])
def list_courses():
    cat = request.args.get("category")
    diff = request.args.get("difficulty")
    return jsonify(CourseService.get_all_courses(category=cat, difficulty=diff)), 200

@course_bp.route("/courses/<slug>", methods=["GET"])
def get_course(slug):
    c = CourseService.get_course_by_slug(slug)
    if not c:
        return jsonify({"error": "Course not found."}), 404
    return jsonify(c), 200

@course_bp.route("/courses/<int:course_id>/lessons/<int:lesson_id>/complete", methods=["POST"])
@require_auth
def complete_lesson(course_id, lesson_id):
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    score = float(data.get("score", 100.0))
    res = CourseService.complete_lesson(user_id=user_id, course_id=course_id, lesson_id=lesson_id, score=score)
    return jsonify(res), 200

@course_bp.route("/learning/skills", methods=["GET"])
def get_skills():
    payload = authenticate_request()
    uid = payload.get("user_id") if payload else None
    return jsonify(LearningService.get_skill_tree(user_id=uid)), 200
