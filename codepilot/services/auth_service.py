"""
CodePilot Authentication Service in Python
"""

import hashlib
import time
from typing import Optional, Dict
from codepilot.models.user import User, UserRole

class AuthServicePython:
    def __init__(self):
        self.users_db: Dict[str, User] = {}
        # Pre-seed default user
        demo_user = User(
            id="u_demo123",
            name="Alex Developer",
            username="alex_dev",
            email="alex.developer@codepilot.io",
            role=UserRole.STUDENT,
            rating=1845,
            xp=4250
        )
        self.users_db[demo_user.email] = demo_user

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def login(self, email: str, password: str) -> Optional[User]:
        if email in self.users_db:
            return self.users_db[email]
        return None

    def register(self, name: str, username: str, email: str, password: str) -> User:
        if email in self.users_db:
            raise ValueError("Email already registered.")
        
        new_user = User(
            id=f"u_{int(time.time())}",
            name=name,
            username=username,
            email=email,
            role=UserRole.STUDENT,
            rating=1500,
            xp=100
        )
        self.users_db[email] = new_user
        return new_user
