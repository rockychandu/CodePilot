"""
Project Workspace Domain Service
"""

from typing import Optional, List, Dict, Any
from backend.repositories.project_repository import ProjectRepository
from backend.repositories.history_repository import HistoryRepository

class ProjectService:
    @staticmethod
    def get_user_projects(user_id: int) -> List[Dict[str, Any]]:
        return ProjectRepository.get_user_projects(user_id)

    @staticmethod
    def get_project_details(project_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        return ProjectRepository.get_project_details(project_id, user_id)

    @staticmethod
    def create_project(user_id: int, title: str, description: str = "", language: str = "python", template: str = "basic") -> Dict[str, Any]:
        proj = ProjectRepository.create_project(user_id, title, description, language, template)
        HistoryRepository.record_activity(
            user_id=user_id,
            activity_type="PROJECT",
            title=f"Created Project '{title}'",
            description=f"Language: {language} | Template: {template}",
            language=language,
            details={"projectId": proj["id"]}
        )
        return proj

    @staticmethod
    def update_project_file(project_id: int, user_id: int, filename: str, content: str) -> bool:
        return ProjectRepository.update_file(project_id, user_id, filename, content)
