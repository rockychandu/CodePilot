"""
Project Workspaces API Blueprint (/api/v1/projects)
"""

from flask import Blueprint, request, jsonify
from backend.projects.project_service import ProjectService
from backend.middleware.auth_middleware import require_auth

project_bp = Blueprint("project_bp", __name__, url_prefix="/api/v1/projects")

@project_bp.route("", methods=["GET"])
@require_auth
def list_projects():
    user_id = request.user_payload["user_id"]
    return jsonify(ProjectService.get_user_projects(user_id)), 200

@project_bp.route("", methods=["POST"])
@require_auth
def create_project():
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    title = data.get("title", "Untitled Project")
    description = data.get("description", "")
    language = data.get("language", "python")
    template = data.get("template", "basic")

    proj = ProjectService.create_project(user_id=user_id, title=title, description=description, language=language, template=template)
    return jsonify(proj), 201

@project_bp.route("/<int:project_id>", methods=["GET"])
@require_auth
def get_project(project_id):
    user_id = request.user_payload["user_id"]
    proj = ProjectService.get_project_details(project_id, user_id)
    if not proj:
        return jsonify({"error": "Project not found or private."}), 404
    return jsonify(proj), 200

@project_bp.route("/<int:project_id>/files", methods=["PUT"])
@require_auth
def update_project_file(project_id):
    user_id = request.user_payload["user_id"]
    data = request.get_json() or {}
    filename = data.get("filename", "")
    content = data.get("content", "")

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    success = ProjectService.update_project_file(project_id, user_id, filename, content)
    if not success:
        return jsonify({"error": "Failed to update project file."}), 400
    return jsonify({"message": "File updated successfully."}), 200
