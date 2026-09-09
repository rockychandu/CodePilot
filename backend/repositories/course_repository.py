"""
Course & Learning Repository
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import Course, Module, Lesson, LearningProgress

class CourseRepository:
    @staticmethod
    def get_all(category: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(Course).filter(Course.is_published == True)
            if category and category.lower() != "all":
                query = query.filter(Course.category.ilike(category))
            if difficulty and difficulty.lower() != "all":
                query = query.filter(Course.difficulty.ilike(difficulty))
            courses = query.order_by(Course.id.asc()).all()
            return [c.to_dict(include_modules=False) for c in courses]

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            course = db.query(Course).filter(Course.slug == slug).first()
            if not course:
                return None
            return course.to_dict(include_modules=True)

    @staticmethod
    def mark_lesson_complete(user_id: int, course_id: int, lesson_id: int, score: float = 100.0) -> Dict[str, Any]:
        with get_db_session() as db:
            progress = db.query(LearningProgress).filter(
                LearningProgress.user_id == user_id,
                LearningProgress.lesson_id == lesson_id
            ).first()

            if not progress:
                progress = LearningProgress(
                    user_id=user_id,
                    course_id=course_id,
                    lesson_id=lesson_id,
                    is_completed=True,
                    completed_at=datetime.now(timezone.utc),
                    score=score
                )
                db.add(progress)
            else:
                progress.is_completed = True
                progress.completed_at = datetime.now(timezone.utc)
                progress.score = max(progress.score, score)

            db.commit()
            return {
                "courseId": course_id,
                "lessonId": lesson_id,
                "isCompleted": True,
                "score": score
            }
