"""
Input Sanitizer & XSS Prevention Utility
"""
import re
import html

class InputSanitizer:
    DANGEROUS_TAGS_PATTERN = re.compile(r"<\s*(script|iframe|object|embed|style|meta|link)[^>]*>.*?<\s*/\s*\1\s*>", re.IGNORECASE | re.DOTALL)
    SELF_CLOSING_DANGEROUS = re.compile(r"<\s*(script|iframe|object|embed|style|meta|link)[^>]*/>", re.IGNORECASE)
    ON_ATTRIBUTES_PATTERN = re.compile(r"\s+on\w+\s*=\s*[\x22\x27][^\x22\x27]*[\x22\x27]", re.IGNORECASE)
    JAVASCRIPT_URI_PATTERN = re.compile(r"javascript\s*:\s*", re.IGNORECASE)

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        if not text:
            return ""
        s = cls.DANGEROUS_TAGS_PATTERN.sub("", text)
        s = cls.SELF_CLOSING_DANGEROUS.sub("", s)
        s = cls.ON_ATTRIBUTES_PATTERN.sub("", s)
        s = cls.JAVASCRIPT_URI_PATTERN.sub("", s)
        return s.strip()

    @classmethod
    def escape_html(cls, text: str) -> str:
        return html.escape(text or "")
