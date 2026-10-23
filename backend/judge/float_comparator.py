"""
Floating-Point Epsilon Judge Comparator
"""
import math

class FloatComparator:
    DEFAULT_EPSILON = 1e-6

    @classmethod
    def compare_tokens(cls, expected_token: str, actual_token: str, epsilon: float = None) -> bool:
        eps = epsilon if epsilon is not None else cls.DEFAULT_EPSILON
        try:
            exp_val = float(expected_token)
            act_val = float(actual_token)
            diff = abs(exp_val - act_val)
            if diff <= eps:
                return True
            # Relative check
            denom = max(abs(exp_val), abs(act_val))
            if denom > 0 and (diff / denom) <= eps:
                return True
            return False
        except ValueError:
            return expected_token.strip() == actual_token.strip()
