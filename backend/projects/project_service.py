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
    def create_project(user_id: int, title: str, description: str = "", language: str = "python", template: str = "cli") -> Dict[str, Any]:
        proj = ProjectRepository.create_project(user_id, title, description, language, template)
        HistoryRepository.record_activity(
            user_id=user_id,
            activity_type="PROJECT",
            title=f"Created Workspace '{title}'",
            description=f"Language: {language.capitalize()} | Template: {template.capitalize()}",
            language=language,
            details={"projectId": proj["id"], "fileCount": proj.get("fileCount", 1)}
        )
        return proj

    @staticmethod
    def rename_project(project_id: int, user_id: int, title: str, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        return ProjectRepository.rename_project(project_id, user_id, title, description)

    @staticmethod
    def duplicate_project(project_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        proj = ProjectRepository.duplicate_project(project_id, user_id)
        if proj:
            HistoryRepository.record_activity(
                user_id=user_id,
                activity_type="PROJECT",
                title=f"Duplicated Workspace '{proj['title']}'",
                description=f"Cloned workspace ID {project_id}",
                language=proj.get("primaryLanguage", "python"),
                details={"projectId": proj["id"]}
            )
        return proj

    @staticmethod
    def delete_project(project_id: int, user_id: int) -> bool:
        return ProjectRepository.delete_project(project_id, user_id)

    @staticmethod
    def update_project_file(project_id: int, user_id: int, filename: str, content: str) -> bool:
        return ProjectRepository.update_file(project_id, user_id, filename, content)

    @staticmethod
    def delete_project_file(project_id: int, user_id: int, filename: str) -> bool:
        return ProjectRepository.delete_file(project_id, user_id, filename)

    @staticmethod
    def export_project(project_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        proj = ProjectRepository.get_project_details(project_id, user_id)
        if not proj:
            return None
        return {
            "version": "1.0",
            "exportedAt": proj.get("updatedAt"),
            "project": {
                "id": proj["id"],
                "title": proj["title"],
                "description": proj["description"],
                "primaryLanguage": proj["primaryLanguage"],
                "fileCount": proj["fileCount"],
                "files": proj.get("files", [])
            }
        }
