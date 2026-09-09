"""
CodePilot Submissions Data Model in Python
"""

from dataclasses import dataclass
from enum import Enum
import time

class SubmissionStatus(Enum):
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    RUNTIME_ERROR = "Runtime Error"
    COMPILATION_ERROR = "Compilation Error"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"

@dataclass
class Submission:
    id: str
    problem_id: str
    user_id: str
    language: str
    source_code: str
    status: SubmissionStatus
    runtime: str
    memory: str
    submitted_at: float = time.time()

    def to_dict(self):
        return {
            "id": self.id,
            "problemId": self.problem_id,
            "userId": self.user_id,
            "language": self.language,
            "sourceCode": self.source_code,
            "status": self.status.value,
            "runtime": self.runtime,
            "memory": self.memory,
            "submittedAt": self.submitted_at
        }
