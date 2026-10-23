import unittest
import time
from backend.middleware.trace_middleware import TraceContext

class TestTraceMiddleware(unittest.TestCase):
    def test_trace_id_format(self):
        tid = TraceContext.generate_trace_id()
        self.assertTrue(tid.startswith("trace-"))
        self.assertTrue(len(tid) > 10)

    def test_trace_headers(self):
        start = time.time() - 0.05
        headers = TraceContext.build_trace_headers("test-trace-123", start)
        self.assertEqual(headers["X-Request-ID"], "test-trace-123")
        self.assertTrue(float(headers["X-Response-Time-Ms"]) >= 40.0)

    def test_uniqueness(self):
        tids = {TraceContext.generate_trace_id() for _ in range(50)}
        self.assertEqual(len(tids), 50)

if __name__ == "__main__":
    unittest.main()
