"""
Session Token & JWT Lifecycle Management
"""

import time
import json
import base64
import hmac
import hashlib
import secrets
from typing import Optional, Dict, Any
from backend.config.settings import settings

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _base64url_decode(data: str) -> bytes:
    padding = '=' * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)

def create_access_token(user_id: int, username: str, role: str, expires_in_hours: Optional[int] = None) -> str:
    """Generate signed JWT access token with unique identifier."""
    exp_hours = expires_in_hours or settings.JWT_EXPIRATION_HOURS
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "jti": secrets.token_hex(8),
        "iat": int(time.time()),
        "exp": int(time.time()) + (exp_hours * 3600)
    }

    header_bytes = json.dumps(header, separators=(',', ':')).encode('utf-8')
    payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')

    segments = [
        _base64url_encode(header_bytes),
        _base64url_encode(payload_bytes)
    ]
    signing_input = f"{segments[0]}.{segments[1]}".encode('utf-8')
    signature = hmac.new(settings.JWT_SECRET.encode('utf-8'), signing_input, hashlib.sha256).digest()
    segments.append(_base64url_encode(signature))

    return ".".join(segments)

def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify cryptographic signature and expiration."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None

        signing_input = f"{parts[0]}.{parts[1]}".encode('utf-8')
        expected_sig = hmac.new(settings.JWT_SECRET.encode('utf-8'), signing_input, hashlib.sha256).digest()
        provided_sig = _base64url_decode(parts[2])

        if not hmac.compare_digest(expected_sig, provided_sig):
            return None

        payload_bytes = _base64url_decode(parts[1])
        payload = json.loads(payload_bytes.decode('utf-8'))

        if time.time() > payload.get("exp", 0):
            return None

        return payload
    except Exception:
        return None

def generate_refresh_token() -> str:
    """Generate cryptographically strong random refresh token."""
    return secrets.token_urlsafe(48)
