"""
Temporary Workspace Isolation and RAII Directory Manager
"""
import os
import shutil
import tempfile

class IsolatedWorkspace:
    def __init__(self, prefix="codepilot_run_"):
        self.prefix = prefix
        self.path = None

    def __enter__(self):
        self.path = tempfile.mkdtemp(prefix=self.prefix)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and os.path.exists(self.path):
            shutil.rmtree(self.path, ignore_errors=True)

    def write_file(self, rel_path: str, content: str) -> str:
        safe_rel = rel_path.replace(chr(92), "/").lstrip("/")
        full_path = os.path.join(self.path, safe_rel)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path
