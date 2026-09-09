"""
CodePilot Project Workspace Service
Manages multi-file developer workspaces, file trees, project settings, and templates.
"""

from codepilot.db.connection import db_session
from codepilot.db.models import Project, ProjectFile, User


class ProjectService:
    @staticmethod
    def get_user_projects(user_id: int) -> list[dict]:
        db = db_session()
        projects = db.query(Project).filter_by(user_id=user_id).order_by(Project.updated_at.desc()).all()
        return [p.to_dict(include_files=False) for p in projects]

    @staticmethod
    def get_project_details(project_id: int, user_id: int = None) -> dict | None:
        db = db_session()
        query = db.query(Project).filter_by(id=project_id)
        if user_id:
            query = query.filter((Project.user_id == user_id) | (Project.is_public == True))
        proj = query.first()
        if not proj:
            return None
        return proj.to_dict(include_files=True)

    @staticmethod
    def create_project(user_id: int, title: str, description: str = "", language: str = "python", template: str = "basic") -> dict:
        db = db_session()
        proj = Project(
            user_id=user_id,
            title=title,
            description=description,
            primary_language=language,
            is_public=False
        )
        db.add(proj)
        db.flush()

        # Seed initial starter files based on template
        if language == "python":
            main_file = ProjectFile(
                project_id=proj.id,
                filename="main.py",
                file_path="main.py",
                content='"""CodePilot Project Main Entrypoint"""\n\ndef main():\n    print("Welcome to your CodePilot Project!")\n\nif __name__ == "__main__":\n    main()\n'
            )
            readme_file = ProjectFile(
                project_id=proj.id,
                filename="README.md",
                file_path="README.md",
                content=f"# {title}\n\n{description}\n"
            )
            db.add_all([main_file, readme_file])
        elif language == "javascript":
            main_file = ProjectFile(
                project_id=proj.id,
                filename="index.js",
                file_path="index.js",
                content='// CodePilot Project\nconsole.log("Hello from CodePilot JS Project!");\n'
            )
            db.add(main_file)

        db.commit()
        return proj.to_dict(include_files=True)

    @staticmethod
    def update_project_file(project_id: int, user_id: int, filename: str, content: str) -> bool:
        db = db_session()
        proj = db.query(Project).filter_by(id=project_id, user_id=user_id).first()
        if not proj:
            return False

        file_entry = db.query(ProjectFile).filter_by(project_id=project_id, filename=filename).first()
        if file_entry:
            file_entry.content = content
        else:
            file_entry = ProjectFile(
                project_id=project_id,
                filename=filename,
                file_path=filename,
                content=content
            )
            db.add(file_entry)

        db.commit()
        return True
