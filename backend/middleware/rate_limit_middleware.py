"""
Rate Limiting Middleware for Flask API
"""

from functools import wraps
from flask import request, jsonify
from backend.security.rate_limiter import rate_limiter

def limit_requests(max_per_minute: int = 60):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            client_ip = request.remote_addr or "127.0.0.1"
            auth_header = request.headers.get("Authorization", "")
            key = auth_header if auth_header else client_ip

            if not rate_limiter.is_allowed(key, max_requests=max_per_minute, window_seconds=60):
                return jsonify({
                    "success": False,
                    "error": "Too many requests. Please slow down.",
                    "retryAfterSeconds": 60
                }), 429

            return f(*args, **kwargs)
        return decorated
    return decorator
