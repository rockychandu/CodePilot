"""
CodePilot User & Profile Data Models in Python
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
import time

class UserRole(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

@dataclass
class Badge:
    id: str
    title: str
    description: str
    icon: str
    unlocked_at: str

@dataclass
class User:
    id: str
    name: str
    username: str
    email: str
    role: UserRole = UserRole.STUDENT
    avatar: str = ""
    rating: int = 1500
    xp: int = 0
    level: int = 1
    streak: int = 1
    solved_count: int = 0
    bio: str = ""
    badges: List[Badge] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "avatar": self.avatar,
            "rating": self.rating,
            "xp": self.xp,
            "level": self.level,
            "streak": self.streak,
            "solvedCount": self.solved_count,
            "bio": self.bio
        }

    def add_xp(self, amount: int):
        self.xp += amount
        # Level up formula: 1 level per 500 XP
        self.level = (self.xp // 500) + 1
