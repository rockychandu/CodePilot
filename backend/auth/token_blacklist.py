"""
In-Memory Thread-Safe JWT Token Revocation Registry
"""
import time
import threading

class TokenBlacklist:
    def __init__(self):
        self._revoked = {}  # token_hash -> expiry_timestamp
        self._lock = threading.Lock()

    def revoke(self, token_identifier: str, expires_at: float = None):
        if expires_at is None:
            expires_at = time.time() + 86400  # Default 24 hours
        with self._lock:
            self._revoked[token_identifier] = expires_at

    def is_revoked(self, token_identifier: str) -> bool:
        now = time.time()
        with self._lock:
            exp = self._revoked.get(token_identifier)
            if exp is None:
                return False
            if exp < now:
                del self._revoked[token_identifier]
                return False
            return True

    def purge_expired(self) -> int:
        now = time.time()
        with self._lock:
            expired = [k for k, exp in self._revoked.items() if exp < now]
            for k in expired:
                del self._revoked[k]
            return len(expired)

token_blacklist = TokenBlacklist()
