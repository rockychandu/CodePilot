"""
Password Security & Cryptography Utilities
Implements salted PBKDF2-HMAC-SHA256 password hashing and strength estimation.
"""

import hashlib
import os
import re
from typing import Tuple, Dict, Any

def generate_salt(length: int = 32) -> str:
    """Generate a secure cryptographic random hex salt."""
    return os.urandom(length).hex()

def hash_password(password: str, salt: str, iterations: int = 100000) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with provided salt."""
    derived = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    )
    return derived.hex()

def verify_password(password: str, salt: str, expected_hash: str, iterations: int = 100000) -> bool:
    """Verify raw password against salt and expected hash in constant time."""
    candidate_hash = hash_password(password, salt, iterations)
    return hashlib.sha256(candidate_hash.encode()).digest() == hashlib.sha256(expected_hash.encode()).digest()

def evaluate_password_strength(password: str) -> Dict[str, Any]:
    """Calculate password strength score (0-100) and feedback criteria."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 25
    else:
        feedback.append("Password should be at least 8 characters long.")

    if len(password) >= 12:
        score += 15

    if re.search(r'[A-Z]', password):
        score += 20
    else:
        feedback.append("Include uppercase letters.")

    if re.search(r'[a-z]', password):
        score += 10
    else:
        feedback.append("Include lowercase letters.")

    if re.search(r'[0-9]', password):
        score += 15
    else:
        feedback.append("Include numbers.")

    if re.search(r'[^A-Za-z0-9]', password):
        score += 15
    else:
        feedback.append("Include special characters.")

    level = "WEAK"
    if score >= 80:
        level = "STRONG"
    elif score >= 50:
        level = "MEDIUM"

    return {
        "score": min(score, 100),
        "level": level,
        "isAcceptable": score >= 50,
        "feedback": feedback
    }
