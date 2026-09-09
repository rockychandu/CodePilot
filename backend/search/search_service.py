"""
Unified Global Search Engine
Indexes and searches across problems, courses, projects, and users.
"""

from typing import Dict, List, Any
from codepilot.db.connection import get_db_session
from codepilot.db.models import Problem, Course, Project, User

class SearchService:
    @staticmethod
    def global_search(query: str, limit_per_type: int = 5) -> Dict[str, Any]:
        query_str = query.strip()
        if not query_str:
            return {"query": "", "problems": [], "courses": [], "projects": [], "totalResults": 0}

        term = f"%{query_str}%"
        with get_db_session() as db:
            # Problems
            problems = db.query(Problem).filter(
                (Problem.title.ilike(term)) | (Problem.description.ilike(term)) | (Problem.tags.ilike(term))
            ).limit(limit_per_type).all()

            # Courses
            courses = db.query(Course).filter(
                (Course.title.ilike(term)) | (Course.description.ilike(term)) | (Course.category.ilike(term))
            ).limit(limit_per_type).all()

            # Public Projects
            projects = db.query(Project).filter(
                Project.is_public == True,
                ((Project.title.ilike(term)) | (Project.description.ilike(term)))
            ).limit(limit_per_type).all()

            prob_list = [p.to_dict() for p in problems]
            course_list = [c.to_dict() for c in courses]
            proj_list = [p.to_dict() for p in projects]
            total = len(prob_list) + len(course_list) + len(proj_list)

            return {
                "query": query_str,
                "problems": prob_list,
                "courses": course_list,
                "projects": proj_list,
                "totalResults": total
            }
