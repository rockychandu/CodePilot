"""
Sliding Window Rate Limiter
Prevents brute force authentication attempts and execution denial-of-service.
"""

import time
import threading
from typing import Dict, List

class RateLimiter:
    def __init__(self, limit_per_minute: int = 120):
        self.limit = limit_per_minute
        self._requests: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, key: str, max_requests: int = None, window_seconds: int = 60) -> bool:
        threshold = max_requests if max_requests is not None else self.limit
        now = time.time()
        window_start = now - window_seconds

        with self._lock:
            timestamps = self._requests.get(key, [])
            # Filter out timestamps outside window
            valid_timestamps = [t for t in timestamps if t > window_start]
            if len(valid_timestamps) >= threshold:
                self._requests[key] = valid_timestamps
                return False
            
            valid_timestamps.append(now)
            self._requests[key] = valid_timestamps
            return True

    def reset(self, key: str) -> None:
        with self._lock:
            if key in self._requests:
                del self._requests[key]

rate_limiter = RateLimiter()
