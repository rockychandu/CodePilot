"""
CodePilot Learning Center & Course Service
Manages courses, lessons, video markers, quizzes, and user completion tracking.
"""

from datetime import datetime, timezone
from codepilot.db.connection import db_session
from codepilot.db.models import Course, Module, Lesson, LearningProgress, Quiz
from codepilot.services.user_service import UserService


class CourseService:
    @staticmethod
    def get_all_courses(category: str = None, difficulty: str = None) -> list[dict]:
        db = db_session()
        query = db.query(Course).filter_by(is_published=True)
        if category:
            query = query.filter_by(category=category)
        if difficulty:
            query = query.filter_by(difficulty=difficulty)
        courses = query.all()
        return [c.to_dict(include_modules=False) for c in courses]

    @staticmethod
    def get_course_by_slug(slug: str) -> dict | None:
        db = db_session()
        course = db.query(Course).filter_by(slug=slug, is_published=True).first()
        if not course:
            return None
        return course.to_dict(include_modules=True)

    @staticmethod
    def complete_lesson(user_id: int, course_id: int, lesson_id: int, score: float = 100.0) -> dict:
        db = db_session()
        prog = db.query(LearningProgress).filter_by(
            user_id=user_id, course_id=course_id, lesson_id=lesson_id
        ).first()

        if not prog:
            prog = LearningProgress(
                user_id=user_id,
                course_id=course_id,
                lesson_id=lesson_id,
                is_completed=True,
                completed_at=datetime.now(timezone.utc),
                score=score
            )
            db.add(prog)
            # Award XP for lesson completion
            UserService.award_xp(user_id, 30)
        else:
            prog.is_completed = True
            prog.completed_at = datetime.now(timezone.utc)
            prog.score = max(prog.score, score)

        db.commit()
        return {"completed": True, "score": prog.score}

    @staticmethod
    def get_user_course_progress(user_id: int, course_id: int) -> dict:
        db = db_session()
        course = db.query(Course).filter_by(id=course_id).first()
        if not course:
            return {"progressPercent": 0, "completedLessons": 0, "totalLessons": 0}

        total_lessons = sum(len(m.lessons) for m in course.modules)
        completed_lessons = db.query(LearningProgress).filter_by(
            user_id=user_id, course_id=course_id, is_completed=True
        ).count()

        percent = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
        return {
            "courseId": course_id,
            "progressPercent": percent,
            "completedLessons": completed_lessons,
            "totalLessons": total_lessons
        }
