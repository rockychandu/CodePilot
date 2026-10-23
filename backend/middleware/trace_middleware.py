"""
Request Trace ID & Execution Latency Middleware Utilities
"""
import uuid
import time

class TraceContext:
    @staticmethod
    def generate_trace_id() -> str:
        return f"trace-{uuid.uuid4().hex}"

    @staticmethod
    def build_trace_headers(trace_id: str, start_time: float) -> dict:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "X-Request-ID": trace_id,
            "X-Response-Time-Ms": str(duration_ms)
        }
