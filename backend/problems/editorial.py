"""
Problem Editorial Solution Markdown Validator
"""
import re

class EditorialValidator:
    REQUIRED_SECTIONS = ["Intuition", "Complexity", "Solution"]

    @classmethod
    def validate_editorial(cls, markdown_text: str) -> dict:
        text = markdown_text or ""
        missing = []
        for sec in cls.REQUIRED_SECTIONS:
            pattern = re.compile(rf"#+\s*{sec}", re.IGNORECASE)
            if not pattern.search(text):
                missing.append(sec)

        has_code_fence = "```" in text
        if not has_code_fence:
            missing.append("Code Snippet (```)")

        return {
            "isValid": len(missing) == 0,
            "missingSections": missing
        }
