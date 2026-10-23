"""
Enterprise Password Policy & Entropy Validation Engine
"""
import math
import re

COMMON_PASSWORDS = {"password", "12345678", "qwerty123", "admin123", "letmein123"}

class PasswordPolicy:
    @staticmethod
    def calculate_entropy(password: str) -> float:
        if not password:
            return 0.0
        pool_size = 0
        if re.search(r"[a-z]", password): pool_size += 26
        if re.search(r"[A-Z]", password): pool_size += 26
        if re.search(r"[0-9]", password): pool_size += 10
        if re.search(r"[^a-zA-Z0-9]", password): pool_size += 32
        if pool_size == 0:
            return 0.0
        return round(len(password) * math.log2(pool_size), 2)

    @classmethod
    def evaluate(cls, password: str) -> dict:
        pwd = password or ""
        issues = []
        if len(pwd) < 8:
            issues.append("Password must be at least 8 characters long.")
        if not re.search(r"[a-z]", pwd):
            issues.append("Missing lowercase letter.")
        if not re.search(r"[A-Z]", pwd):
            issues.append("Missing uppercase letter.")
        if not re.search(r"[0-9]", pwd):
            issues.append("Missing numeric digit.")
        if not re.search(r"[^a-zA-Z0-9]", pwd):
            issues.append("Missing special symbol.")
        if pwd.lower() in COMMON_PASSWORDS:
            issues.append("Password is too common.")

        entropy = cls.calculate_entropy(pwd)
        is_valid = len(issues) == 0
        return {
            "isValid": is_valid,
            "entropyBits": entropy,
            "issues": issues,
            "strength": "STRONG" if entropy >= 50 and is_valid else ("MODERATE" if entropy >= 35 else "WEAK")
        }
