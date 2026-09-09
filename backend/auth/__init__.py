"""
CodePilot Authentication Module
"""

from backend.auth.service import AuthService
from backend.auth.password import generate_salt, hash_password, verify_password, evaluate_password_strength
from backend.auth.tokens import create_access_token, verify_access_token, generate_refresh_token
from backend.auth.validators import validate_username, validate_email, validate_password_match
from backend.auth.rate_limit import auth_rate_limiter, AuthRateLimiter

__all__ = [
    "AuthService",
    "generate_salt",
    "hash_password",
    "verify_password",
    "evaluate_password_strength",
    "create_access_token",
    "verify_access_token",
    "generate_refresh_token",
    "validate_username",
    "validate_email",
    "validate_password_match",
    "auth_rate_limiter",
    "AuthRateLimiter"
]
