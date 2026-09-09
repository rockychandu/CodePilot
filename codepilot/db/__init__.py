"""
CodePilot Database Module
"""

from codepilot.db.connection import engine, db_session, Base, init_db, get_db
from codepilot.db.models import (
    User, Profile, UserSession, PasswordReset, EmailVerification,
    ActivityHistory, CodeExecution, Problem, TestCase, Submission,
    Contest, ContestParticipant, Leaderboard,
    Course, Module, Lesson, LearningProgress, Quiz,
    Skill, UserSkill, Project, ProjectFile,
    AIReview, Notification, AuditLog, RuntimeConfig
)

__all__ = [
    "engine",
    "db_session",
    "Base",
    "init_db",
    "get_db",
    "User",
    "Profile",
    "UserSession",
    "PasswordReset",
    "EmailVerification",
    "ActivityHistory",
    "CodeExecution",
    "Problem",
    "TestCase",
    "Submission",
    "Contest",
    "ContestParticipant",
    "Leaderboard",
    "Course",
    "Module",
    "Lesson",
    "LearningProgress",
    "Quiz",
    "Skill",
    "UserSkill",
    "Project",
    "ProjectFile",
    "AIReview",
    "Notification",
    "AuditLog",
    "RuntimeConfig",
]
