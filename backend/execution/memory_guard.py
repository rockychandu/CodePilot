"""
Execution Memory Bound Watchdog & OOM Trap Handler
"""
class MemoryGuard:
    @staticmethod
    def evaluate_memory_usage(used_bytes: int, limit_bytes: int) -> dict:
        used_mb = round(used_bytes / (1024 * 1024), 2)
        limit_mb = round(limit_bytes / (1024 * 1024), 2)
        exceeded = used_bytes > limit_bytes
        return {
            "isExceeded": exceeded,
            "usedMb": used_mb,
            "limitMb": limit_mb,
            "status": "MEMORY_LIMIT_EXCEEDED" if exceeded else "OK",
            "message": f"Memory limit exceeded: {used_mb}MB / {limit_mb}MB" if exceeded else "Within limits"
        }
