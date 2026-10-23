"""
Process Execution Watchdog Timer & Quotas
"""
class ExecutionWatchdog:
    DEFAULT_TIMEOUT_SEC = 2.0
    MAX_TIMEOUT_SEC = 10.0

    @classmethod
    def check_timeout(cls, elapsed_sec: float, timeout_limit_sec: float = None) -> dict:
        limit = timeout_limit_sec or cls.DEFAULT_TIMEOUT_SEC
        limit = min(limit, cls.MAX_TIMEOUT_SEC)
        timed_out = elapsed_sec > limit
        return {
            "isTimeout": timed_out,
            "elapsedSec": round(elapsed_sec, 3),
            "limitSec": round(limit, 3),
            "status": "TIME_LIMIT_EXCEEDED" if timed_out else "COMPLETED"
        }
