"""
CodePilot Problem Service in Python
"""

from typing import List, Optional, Dict
from codepilot.models.problem import Problem, Difficulty

class ProblemServicePython:
    def __init__(self):
        self.problems: List[Problem] = [
            Problem(
                id="prob_1",
                title="Two Sum (Python Solution)",
                difficulty=Difficulty.EASY,
                category="Algorithms",
                topic="Array & Hash Map",
                acceptance_rate="49.2%",
                solved_count=12450,
                likes=8520,
                description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                examples=[{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}],
                constraints=["2 <= nums.length <= 10^4"],
                hints=["Use a dictionary to check complement in O(1) time."],
                starter_code={"python": "def two_sum(nums, target):\n    pass"}
            )
        ]

    def get_all(self, difficulty: Optional[str] = None, topic: Optional[str] = None, search: Optional[str] = None) -> List[Problem]:
        results = self.problems
        if difficulty:
            results = [p for p in results if p.difficulty.value.lower() == difficulty.lower()]
        if topic:
            results = [p for p in results if topic.lower() in p.topic.lower()]
        if search:
            results = [p for p in results if search.lower() in p.title.lower() or search.lower() in p.description.lower()]
        return results

    def get_by_id(self, problem_id: str) -> Optional[Problem]:
        for p in self.problems:
            if p.id == problem_id:
                return p
        return None
