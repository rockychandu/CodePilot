"""
HTTP Security Headers & CORS Utilities
"""
class SecurityHeaders:
    DEFAULT_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }

    @classmethod
    def apply_security_headers(cls, response_headers: dict) -> dict:
        headers = dict(response_headers or {})
        for k, v in cls.DEFAULT_HEADERS.items():
            headers[k] = v
        return headers

    @staticmethod
    def is_allowed_origin(origin: str, allowed_list: list) -> bool:
        if not origin:
            return False
        if "*" in allowed_list:
            return True
        return origin.rstrip("/") in [o.rstrip("/") for o in allowed_list]
