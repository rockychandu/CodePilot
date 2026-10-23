"""
Glicko-2 Competitive Rating Calculation Engine
"""
import math

class Glicko2:
    @staticmethod
    def calculate_rating_change(current_rating: float, opponent_rating: float, outcome: float, k_factor: float = 32.0) -> float:
        # outcome: 1.0 for win, 0.5 for draw, 0.0 for loss
        expected = 1.0 / (1.0 + 10.0 ** ((opponent_rating - current_rating) / 400.0))
        delta = k_factor * (outcome - expected)
        return round(current_rating + delta, 1)

    @staticmethod
    def adjust_deviation_for_inactivity(rd: float, days_inactive: int, c: float = 3.0) -> float:
        # Rating deviation increases with inactivity
        new_rd = math.sqrt(rd ** 2 + (c ** 2) * days_inactive)
        return round(min(350.0, new_rd), 2)
