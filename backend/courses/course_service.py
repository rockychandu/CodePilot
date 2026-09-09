"""
Course Platform Service
"""

from typing import Optional, List, Dict, Any
from backend.repositories.course_repository import CourseRepository
from backend.repositories.history_repository import HistoryRepository
from backend.repositories.user_repository import UserRepository

class CourseService:
    @staticmethod
    def get_all_courses(category: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        return CourseRepository.get_all(category=category, difficulty=difficulty)

    @staticmethod
    def get_course_by_slug(slug: str) -> Optional[Dict[str, Any]]:
        return CourseRepository.get_by_slug(slug=slug)

    @staticmethod
    def complete_lesson(user_id: int, course_id: int, lesson_id: int, score: float = 100.0) -> Dict[str, Any]:
        res = CourseRepository.mark_lesson_complete(user_id=user_id, course_id=course_id, lesson_id=lesson_id, score=score)
        UserRepository.update_stats(user_id=user_id, xp_gain=25)
        HistoryRepository.record_activity(
            user_id=user_id,
            activity_type="COURSE",
            title="Lesson Completed",
            description=f"Completed lesson #{lesson_id} with score {score:.0f}%",
            details={"courseId": course_id, "lessonId": lesson_id, "score": score}
        )
        return res
