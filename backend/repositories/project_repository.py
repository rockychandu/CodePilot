"""
Project Workspaces Repository
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import Project, ProjectFile

class ProjectRepository:
    @staticmethod
    def get_user_projects(user_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            projects = db.query(Project).filter(Project.user_id == user_id).order_by(Project.updated_at.desc()).all()
            return [p.to_dict(include_files=False) for p in projects]

    @staticmethod
    def get_project_details(project_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            project = db.query(Project).filter(
                Project.id == project_id,
                ((Project.user_id == user_id) | (Project.is_public == True))
            ).first()
            if not project:
                return None
            return project.to_dict(include_files=True)

    @staticmethod
    def create_project(user_id: int, title: str, description: str = "", language: str = "python", template: str = "basic") -> Dict[str, Any]:
        with get_db_session() as db:
            proj = Project(
                user_id=user_id,
                title=title,
                description=description,
                primary_language=language,
                is_public=False
            )
            db.add(proj)
            db.flush()

            # Create default main file
            ext_map = {"python": "main.py", "javascript": "index.js", "cpp": "main.cpp", "java": "Main.java", "c": "main.c", "rust": "main.rs", "go": "main.go"}
            fname = ext_map.get(language.lower(), "main.py")
            default_content = {
                "main.py": "def solve():\n    print('Hello, CodePilot Workspace!')\n\nif __name__ == '__main__':\n    solve()\n",
                "index.js": "function solve() {\n    console.log('Hello, CodePilot Workspace!');\n}\nsolve();\n",
                "Main.java": "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, CodePilot Workspace!\");\n    }\n}\n",
                "main.cpp": "#include <iostream>\n\nint main() {\n    std::cout << \"Hello, CodePilot Workspace!\" << std::endl;\n    return 0;\n}\n",
                "main.c": "#include <stdio.h>\n\nint main() {\n    printf(\"Hello, CodePilot Workspace!\\n\");\n    return 0;\n}\n",
                "main.rs": "fn main() {\n    println!(\"Hello, CodePilot Workspace!\");\n}\n",
                "main.go": "package main\n\nimport \"fmt\"\n\nfunc main() {\n    fmt.Println(\"Hello, CodePilot Workspace!\")\n}\n"
            }.get(fname, "// CodePilot File\n")

            pfile = ProjectFile(
                project_id=proj.id,
                filename=fname,
                file_path=f"/{fname}",
                content=default_content
            )
            db.add(pfile)
            db.commit()
            db.refresh(proj)
            return proj.to_dict(include_files=True)

    @staticmethod
    def update_file(project_id: int, user_id: int, filename: str, content: str) -> bool:
        with get_db_session() as db:
            proj = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
            if not proj:
                return False

            pfile = db.query(ProjectFile).filter(
                ProjectFile.project_id == project_id,
                ProjectFile.filename == filename
            ).first()

            if pfile:
                pfile.content = content
                pfile.updated_at = datetime.now(timezone.utc)
            else:
                pfile = ProjectFile(
                    project_id=project_id,
                    filename=filename,
                    file_path=f"/{filename}",
                    content=content
                )
                db.add(pfile)

            proj.updated_at = datetime.now(timezone.utc)
            db.commit()
            return True
