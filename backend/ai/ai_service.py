"""
Pilot AI Developer Assistant Service
AST parser, bug explanation, complexity estimation, automated unit test generation, refactor advice.
"""

from typing import Dict, Any, Optional
from codepilot.ai.pilot_ai_engine import PilotAIEngine
from backend.repositories.history_repository import HistoryRepository

class AIService:
    @staticmethod
    def review_code(user_id: Optional[int], language: str, source_code: str) -> Dict[str, Any]:
        res = PilotAIEngine.review_code(user_id, language, source_code)
        if user_id:
            HistoryRepository.record_activity(
                user_id=user_id,
                activity_type="AI_REVIEW",
                title=f"AI Code Review ({language.upper()})",
                description=f"Quality Score: {res.get('qualityScore', 85)}/100",
                language=language,
                details=res
            )
        return res

    @staticmethod
    def estimate_complexity(language: str, source_code: str) -> Dict[str, Any]:
        return PilotAIEngine.estimate_complexity(language, source_code)

    @staticmethod
    def generate_tests(user_id: Optional[int], language: str, source_code: str) -> Dict[str, Any]:
        return PilotAIEngine.generate_tests(user_id, language, source_code)

    @staticmethod
    def explain_bug(user_id: Optional[int], language: str, source_code: str, error_message: str = "") -> Dict[str, Any]:
        return PilotAIEngine.explain_bug(user_id, language, source_code, error_message)
