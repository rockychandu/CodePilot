"""
Execution Benchmarking & Statistics Aggregator
"""
import math

class ExecutionBenchmark:
    @staticmethod
    def calculate_stats(timings_ms: list) -> dict:
        if not timings_ms:
            return {"mean": 0.0, "min": 0.0, "max": 0.0, "stddev": 0.0, "count": 0}

        count = len(timings_ms)
        mean_val = sum(timings_ms) / count
        variance = sum((t - mean_val) ** 2 for t in timings_ms) / count
        stddev = math.sqrt(variance)

        return {
            "mean": round(mean_val, 2),
            "min": round(min(timings_ms), 2),
            "max": round(max(timings_ms), 2),
            "stddev": round(stddev, 2),
            "count": count
        }

    @staticmethod
    def calculate_speedup(baseline_ms: float, optimized_ms: float) -> float:
        if optimized_ms <= 0 or baseline_ms <= 0:
            return 1.0
        return round(baseline_ms / optimized_ms, 2)
