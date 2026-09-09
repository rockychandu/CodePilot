"""
Storage & Workspace File Management Service
"""

import os
import shutil
from typing import List, Dict, Any, Optional
from backend.config.settings import settings

class StorageService:
    @classmethod
    def get_user_workspace_dir(cls, user_id: int, project_id: int) -> str:
        path = os.path.join(settings.PROJECT_STORAGE_ROOT, f"user_{user_id}", f"proj_{project_id}")
        os.makedirs(path, exist_ok=True)
        return path

    @classmethod
    def save_file(cls, user_id: int, project_id: int, filename: str, content: str) -> str:
        workspace = cls.get_user_workspace_dir(user_id, project_id)
        clean_name = os.path.basename(filename)
        file_path = os.path.join(workspace, clean_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return file_path

    @classmethod
    def read_file(cls, user_id: int, project_id: int, filename: str) -> Optional[str]:
        workspace = cls.get_user_workspace_dir(user_id, project_id)
        clean_name = os.path.basename(filename)
        file_path = os.path.join(workspace, clean_name)
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def delete_workspace(cls, user_id: int, project_id: int) -> bool:
        workspace = cls.get_user_workspace_dir(user_id, project_id)
        if os.path.exists(workspace):
            shutil.rmtree(workspace, ignore_errors=True)
            return True
        return False
