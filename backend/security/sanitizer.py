"""
Input Sanitization and Defensive Security Helpers
Protects against path traversal, code injection in file paths, and HTML tag injection.
"""

import os
import re
import html

def sanitize_filename(filename: str) -> str:
    """Strip dangerous characters and directory separators from filenames."""
    filename = os.path.basename(filename)
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)
    return filename or "untitled"

def sanitize_text(text: str) -> str:
    """Escape HTML entities in user input."""
    if not text:
        return ""
    return html.escape(text.strip())

def sanitize_code_input(code: str, max_size_bytes: int = 1024 * 1024) -> str:
    """Validate and truncate source code length to prevent memory abuse."""
    if not isinstance(code, str):
        return ""
    if len(code.encode('utf-8')) > max_size_bytes:
        return code[:max_size_bytes]
    return code
