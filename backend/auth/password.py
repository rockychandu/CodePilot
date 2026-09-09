"""
Secure Password Hashing & Verification Engine
Implements salted PBKDF2-HMAC-SHA256 with 100,000 iterations and constant-time comparisons.
"""

import os
import hashlib
import hmac
import re
from typing import Dict, Any, Tuple

ITERATIONS = 100000

def generate_salt(length: int = 32) -> str:
    """Generate cryptographically secure random hexadecimal salt."""
    return os.urandom(length).hex()

def hash_password(password: str, salt: str, iterations: int = ITERATIONS) -> str:
    """Derive key using PBKDF2-HMAC-SHA256."""
    derived = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        iterations
    )
    return derived.hex()

def verify_password(password: str, salt: str, expected_hash: str, iterations: int = ITERATIONS) -> bool:
    """Verify raw password in constant time to prevent timing attacks."""
    candidate_hash = hash_password(password, salt, iterations)
    return hmac.compare_digest(candidate_hash.encode('utf-8'), expected_hash.encode('utf-8'))

def evaluate_password_strength(password: str) -> Dict[str, Any]:
    """Calculate password strength score (0-4) and criteria feedback."""
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters long.")

    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Both uppercase and lowercase letters.")

    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("At least one number.")

    if re.search(r'[^A-Za-z0-9]', password):
        score += 1
    else:
        feedback.append("At least one special character (!@#$%^&*).")

    labels = {0: "Weak", 1: "Weak", 2: "Fair", 3: "Good", 4: "Strong"}

    return {
        "score": score,
        "label": labels.get(score, "Weak"),
        "isAcceptable": score >= 2 and len(password) >= 6,
        "feedback": feedback
    }
