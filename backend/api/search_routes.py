"""
Global Search API Blueprint (/api/v1/search)
"""

from flask import Blueprint, request, jsonify
from backend.search.search_service import SearchService

search_bp = Blueprint("search_bp", __name__, url_prefix="/api/v1/search")

@search_bp.route("", methods=["GET"])
def execute_search():
    q = request.args.get("q", "")
    limit = min(20, int(request.args.get("limit", 5)))
    return jsonify(SearchService.global_search(q, limit_per_type=limit)), 200
