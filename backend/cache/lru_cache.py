"""
Thread-safe In-Memory Cache with LRU eviction and TTL support.
Used for caching leaderboard snapshots, runtime detection reports, and user profile lookups.
"""

import time
import threading
from typing import Any, Optional, Dict, Tuple
from collections import OrderedDict

class MemoryCache:
    def __init__(self, max_size: int = 1000, default_ttl_seconds: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl_seconds
        self._cache: OrderedDict[str, Tuple[Any, float]] = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            val, expire_time = self._cache[key]
            if time.time() > expire_time:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return val

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        with self._lock:
            ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
            expire_time = time.time() + ttl
            if key in self._cache:
                self._cache[key] = (value, expire_time)
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self.max_size:
                    self._cache.popitem(last=False)
                self._cache[key] = (value, expire_time)

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def size(self) -> int:
        with self._lock:
            return len(self._cache)

cache = MemoryCache()
