"""
Interactive Learning and Skill Progress Service
"""

from typing import List, Dict, Any, Optional
from codepilot.db.connection import get_db_session
from codepilot.db.models import Skill, UserSkill

class LearningService:
    @staticmethod
    def get_skill_tree(user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            skills = db.query(Skill).all()
            user_skill_map = {}
            if user_id:
                user_skills = db.query(UserSkill).filter(UserSkill.user_id == user_id).all()
                user_skill_map = {us.skill_slug: us for us in user_skills}

            tree = []
            for s in skills:
                data = s.to_dict()
                us = user_skill_map.get(s.slug)
                data["userLevel"] = us.current_level if us else 1
                data["userXp"] = us.xp if us else 0
                tree.append(data)

            return tree
