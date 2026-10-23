"""
Tiered Sliding-Window Rate Limiter Engine
"""
import time
import threading

TIER_LIMITS = {
    "GUEST": 30,
    "USER": 120,
    "ADMIN": 600
}

class TieredRateLimiter:
    def __init__(self):
        self._history = {}
        self._lock = threading.Lock()

    def allow_request(self, client_id: str, tier: str = "USER", window_seconds: int = 60) -> tuple:
        max_requests = TIER_LIMITS.get(tier.upper(), 60)
        now = time.time()
        window_start = now - window_seconds

        with self._lock:
            timestamps = self._history.setdefault(client_id, [])
            self._history[client_id] = [t for t in timestamps if t > window_start]
            current_count = len(self._history[client_id])

            if current_count >= max_requests:
                retry_after = round(self._history[client_id][0] + window_seconds - now, 1)
                return False, max(1, int(retry_after))

            self._history[client_id].append(now)
            return True, 0
