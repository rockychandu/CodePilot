"""
Authentication & RBAC Middleware Decorators
"""

from functools import wraps
from flask import request, jsonify
from backend.security.jwt_tokens import verify_access_token
from codepilot.db.connection import get_db_session
from codepilot.db.models import UserSession

def get_token_from_header():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    return None

def authenticate_request():
    token = get_token_from_header()
    if not token:
        return None
    
    payload = verify_access_token(token)
    if not payload:
        return None

    # Check session revocation in database
    try:
        with get_db_session() as db:
            session_rec = db.query(UserSession).filter(
                UserSession.token == token,
                UserSession.is_revoked == False
            ).first()
            if not session_rec:
                return None
    except Exception:
        # Fallback to stateless validation if db lookup encounters transient error
        pass

    return payload

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = authenticate_request()
        if not payload:
            return jsonify({
                "success": False,
                "error": "Unauthorized. A valid Bearer token is required."
            }), 401
        request.user_payload = payload
        return f(*args, **kwargs)
    return decorated

def require_role(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            payload = authenticate_request()
            if not payload:
                return jsonify({
                    "success": False,
                    "error": "Unauthorized."
                }), 401
            
            user_role = payload.get("role", "USER")
            if user_role not in roles and "ADMIN" not in user_role:
                return jsonify({
                    "success": False,
                    "error": f"Forbidden. Role must be one of: {', '.join(roles)}"
                }), 403
            
            request.user_payload = payload
            return f(*args, **kwargs)
        return decorated
    return decorator
