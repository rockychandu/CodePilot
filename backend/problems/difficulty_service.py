"""
Problem Difficulty Calculator & Acceptance Statistics
"""
class DifficultyService:
    @staticmethod
    def calculate_difficulty(total_submissions: int, accepted_submissions: int) -> dict:
        if total_submissions <= 0:
            return {"acceptanceRate": 0.0, "difficulty": "MEDIUM", "total": 0, "accepted": 0}

        acc = max(0, min(total_submissions, accepted_submissions))
        rate = round((acc / total_submissions) * 100, 1)

        if rate >= 60.0:
            diff = "EASY"
        elif rate >= 30.0:
            diff = "MEDIUM"
        else:
            diff = "HARD"

        return {
            "acceptanceRate": rate,
            "difficulty": diff,
            "total": total_submissions,
            "accepted": acc
        }
