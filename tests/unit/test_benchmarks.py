import unittest
from backend.execution.benchmarks import ExecutionBenchmark

class TestBenchmarks(unittest.TestCase):
    def test_stats_computation(self):
        timings = [10.0, 12.0, 14.0]
        stats = ExecutionBenchmark.calculate_stats(timings)
        self.assertEqual(stats["mean"], 12.0)
        self.assertEqual(stats["min"], 10.0)
        self.assertEqual(stats["max"], 14.0)
        self.assertEqual(stats["count"], 3)

    def test_speedup(self):
        speedup = ExecutionBenchmark.calculate_speedup(100.0, 50.0)
        self.assertEqual(speedup, 2.0)

    def test_empty_stats(self):
        stats = ExecutionBenchmark.calculate_stats([])
        self.assertEqual(stats["count"], 0)
        self.assertEqual(stats["mean"], 0.0)

if __name__ == "__main__":
    unittest.main()
