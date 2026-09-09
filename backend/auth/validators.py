"""
Authentication Request Validators
"""

import re
from typing import Tuple, Optional

def validate_username(username: str) -> Tuple[bool, Optional[str]]:
    if not username or len(username.strip()) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username.strip()) > 32:
        return False, "Username must not exceed 32 characters."
    if not re.match(r'^[a-zA-Z0-9_.-]+$', username.strip()):
        return False, "Username can only contain alphanumeric characters, underscores, dots, and dashes."
    return True, None

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    if not email or len(email.strip()) < 5:
        return False, "Email address is required."
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email.strip()):
        return False, "Please enter a valid email address."
    return True, None

def validate_password_match(password: str, confirm_password: str) -> Tuple[bool, Optional[str]]:
    if not password:
        return False, "Password is required."
    if password != confirm_password:
        return False, "Passwords do not match."
    return True, None
