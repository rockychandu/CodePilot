"""
CodePilot Security & Cryptography Utilities
Implements PBKDF2-HMAC-SHA256 password hashing with cryptographic salts,
secure tokens, and HMAC-SHA256 based JWT token signing and verification.
"""

import os
import hmac
import hashlib
import base64
import json
import time
from datetime import datetime, timezone, timedelta

SECRET_KEY = os.environ.get("CODEPILOT_SECRET_KEY", "codepilot-super-secret-jwt-key-2026-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", "30"))


def generate_salt(length=32) -> str:
    """Generate cryptographically secure hexadecimal salt."""
    return os.urandom(length).hex()


def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash password using PBKDF2-HMAC-SHA256 with 100,000 iterations."""
    if salt is None:
        salt = generate_salt()
    pwd_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    hashed = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100_000)
    return hashed.hex(), salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    """Verify raw password against salt and stored hash."""
    new_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(new_hash, password_hash)


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')


def _base64url_decode(data_str: str) -> bytes:
    padding = '=' * (4 - len(data_str) % 4) if len(data_str) % 4 != 0 else ''
    return base64.urlsafe_b64decode(data_str + padding)


def create_access_token(user_id: int, username: str, role: str = "USER", expires_delta: timedelta = None) -> str:
    """Create signed JWT access token."""
    header = {"alg": "HS256", "typ": "JWT"}
    now = int(time.time())
    if expires_delta:
        exp = now + int(expires_delta.total_seconds())
    else:
        exp = now + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    payload = {
        "sub": str(user_id),
        "user_id": user_id,
        "username": username,
        "role": role,
        "iat": now,
        "exp": exp
    }

    header_b64 = _base64url_encode(json.dumps(header).encode('utf-8'))
    payload_b64 = _base64url_encode(json.dumps(payload).encode('utf-8'))
    signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')

    signature = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    sig_b64 = _base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{sig_b64}"


def create_refresh_token(user_id: int) -> str:
    """Create secure refresh token."""
    random_part = os.urandom(32).hex()
    return f"rt_{user_id}_{random_part}"


def verify_token(token: str) -> dict | None:
    """Verify and decode JWT token. Returns payload dict or None if invalid/expired."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts

        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        actual_sig = _base64url_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = _base64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))

        # Expiration check
        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload
    except Exception:
        return None
