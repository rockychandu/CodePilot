"""
CodePilot Problem & TestCase Data Models in Python
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

@dataclass
class TestCase:
    input_data: str
    expected_output: str
    is_hidden: bool = False

@dataclass
class Problem:
    id: str
    title: str
    difficulty: Difficulty
    category: str
    topic: str
    acceptance_rate: str
    solved_count: int
    likes: int
    description: str
    examples: List[Dict[str, str]]
    constraints: List[str]
    hints: List[str]
    starter_code: Dict[str, str]
    test_cases: List[TestCase] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "difficulty": self.difficulty.value,
            "category": self.category,
            "topic": self.topic,
            "acceptanceRate": self.acceptance_rate,
            "solvedCount": self.solved_count,
            "likes": self.likes,
            "description": self.description,
            "examples": self.examples,
            "constraints": self.constraints,
            "hints": self.hints,
            "starterCode": self.starter_code
        }
