"""
CodePilot Database Models (SQLAlchemy ORM)
Enterprise schema for users, authentication, code execution, competitive programming,
Pilot AI assistant, learning platform, project workspaces, and system analytics.
"""

from datetime import datetime, timezone
import json
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from codepilot.db.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    salt = Column(String(64), nullable=False)
    role = Column(String(32), default="USER", nullable=False)  # USER, MODERATOR, INSTRUCTOR, ADMIN
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    settings = relationship("UserSettings", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    executions = relationship("CodeExecution", back_populates="user", cascade="all, delete-orphan")
    activities = relationship("ActivityHistory", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    user_skills = relationship("UserSkill", back_populates="user", cascade="all, delete-orphan")
    learning_progress = relationship("LearningProgress", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self, include_private=False):
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email if include_private else None,
            "role": self.role,
            "isActive": self.is_active,
            "isVerified": self.is_verified,
            "lastLoginAt": self.last_login_at.isoformat() if self.last_login_at else None,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
        if self.profile:
            data["profile"] = self.profile.to_dict()
        if self.settings and include_private:
            data["settings"] = self.settings.to_dict()
        return data


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    display_name = Column(String(128), nullable=True)
    avatar_url = Column(String(256), default="frontend/assets/logo.svg")
    bio = Column(Text, default="")
    primary_language = Column(String(32), default="Python")
    preferred_languages = Column(Text, default="[\"Python\", \"JavaScript\"]")  # JSON encoded list
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    rank_title = Column(String(64), default="Novice Explorer")
    streak_days = Column(Integer, default=0)
    problems_solved = Column(Integer, default=0)
    contest_rating = Column(Integer, default=1200)
    courses_completed = Column(Integer, default=0)
    achievements = Column(Text, default="[]")  # JSON encoded list of achievement IDs
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="profile")

    def to_dict(self):
        try:
            langs = json.loads(self.preferred_languages)
        except Exception:
            langs = ["Python"]
        try:
            achieves = json.loads(self.achievements)
        except Exception:
            achieves = []

        return {
            "userId": self.user_id,
            "displayName": self.display_name or (self.user.username if self.user else "User"),
            "avatarUrl": self.avatar_url,
            "bio": self.bio,
            "primaryLanguage": self.primary_language,
            "preferredLanguages": langs,
            "xp": self.xp,
            "level": self.level,
            "rankTitle": self.rank_title,
            "streakDays": self.streak_days,
            "problemsSolved": self.problems_solved,
            "contestRating": self.contest_rating,
            "coursesCompleted": self.courses_completed,
            "achievements": achieves,
        }


class UserSession(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token = Column(String(256), unique=True, nullable=False, index=True)
    refresh_token = Column(String(256), unique=True, nullable=True)
    ip_address = Column(String(64), nullable=True)
    user_agent = Column(String(256), nullable=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="sessions")


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reset_token = Column(String(128), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utc_now)


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    verification_token = Column(String(128), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utc_now)


class ActivityHistory(Base):
    __tablename__ = "activity_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    activity_type = Column(String(64), nullable=False, index=True)  # EXECUTION, SUBMISSION, CONTEST, AI_REVIEW, COURSE, SKILL, LOGIN
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    language = Column(String(32), nullable=True, index=True)
    status = Column(String(32), nullable=True)
    details_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="activities")

    def to_dict(self):
        try:
            meta = json.loads(self.details_json)
        except Exception:
            meta = {}
        return {
            "id": self.id,
            "userId": self.user_id,
            "activityType": self.activity_type,
            "title": self.title,
            "description": self.description,
            "language": self.language,
            "status": self.status,
            "details": meta,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class CodeExecution(Base):
    __tablename__ = "code_executions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    language = Column(String(32), nullable=False, index=True)
    source_code = Column(Text, nullable=False)
    stdin = Column(Text, default="")
    stdout = Column(Text, default="")
    stderr = Column(Text, default="")
    status = Column(String(32), nullable=False)  # ACCEPTED, COMPILE_ERROR, RUNTIME_ERROR, TIME_LIMIT_EXCEEDED
    runtime_seconds = Column(Float, default=0.0)
    memory_mb = Column(Float, default=0.0)
    exit_code = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="executions")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "language": self.language,
            "sourceCode": self.source_code,
            "stdin": self.stdin,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "status": self.status,
            "runtime": f"{self.runtime_seconds:.3f}s",
            "memory": f"{self.memory_mb:.1f} MB",
            "exitCode": self.exit_code,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    difficulty = Column(String(32), nullable=False, index=True)  # Easy, Medium, Hard
    category = Column(String(64), nullable=False, index=True)    # Algorithms, Data Structures, Math, etc.
    tags = Column(Text, default="[]")                           # JSON list of tags
    description = Column(Text, nullable=False)
    constraints = Column(Text, default="")
    hints = Column(Text, default="[]")                           # JSON list of hints
    editorial = Column(Text, default="")
    starter_templates = Column(Text, default="{}")               # JSON dict { "python": "...", "javascript": "..." }
    time_limit_seconds = Column(Float, default=2.0)
    memory_limit_mb = Column(Float, default=128.0)
    total_submissions = Column(Integer, default=0)
    accepted_submissions = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")

    def to_dict(self, include_test_cases=False, include_hidden=False):
        try:
            tags = json.loads(self.tags)
        except Exception:
            tags = []
        try:
            hints = json.loads(self.hints)
        except Exception:
            hints = []
        try:
            templates = json.loads(self.starter_templates)
        except Exception:
            templates = {}

        data = {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "difficulty": self.difficulty,
            "category": self.category,
            "tags": tags,
            "description": self.description,
            "constraints": self.constraints,
            "hints": hints,
            "editorial": self.editorial,
            "starterTemplates": templates,
            "timeLimit": self.time_limit_seconds,
            "memoryLimit": self.memory_limit_mb,
            "totalSubmissions": self.total_submissions,
            "acceptedSubmissions": self.accepted_submissions,
            "acceptanceRate": f"{(self.accepted_submissions / self.total_submissions * 100):.1f}%" if self.total_submissions > 0 else "0.0%",
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
        if include_test_cases:
            tc_list = []
            for tc in self.test_cases:
                if not tc.is_hidden or include_hidden:
                    tc_list.append(tc.to_dict())
            data["testCases"] = tc_list
        return data


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)
    explanation = Column(Text, default="")
    order_index = Column(Integer, default=0)

    problem = relationship("Problem", back_populates="test_cases")

    def to_dict(self):
        return {
            "id": self.id,
            "problemId": self.problem_id,
            "input": self.input_data,
            "expectedOutput": self.expected_output,
            "isHidden": self.is_hidden,
            "explanation": self.explanation,
        }


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True)
    contest_id = Column(Integer, ForeignKey("contests.id", ondelete="SET NULL"), nullable=True, index=True)
    language = Column(String(32), nullable=False, index=True)
    source_code = Column(Text, nullable=False)
    status = Column(String(32), nullable=False, index=True)  # Accepted, Wrong Answer, Compilation Error, Time Limit Exceeded, Runtime Error
    passed_tests = Column(Integer, default=0)
    total_tests = Column(Integer, default=0)
    runtime_seconds = Column(Float, default=0.0)
    memory_mb = Column(Float, default=0.0)
    compiler_output = Column(Text, default="")
    test_results_json = Column(Text, default="[]")  # JSON list of per-test results
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
    contest = relationship("Contest", back_populates="submissions")

    def to_dict(self):
        try:
            results = json.loads(self.test_results_json)
        except Exception:
            results = []
        return {
            "id": self.id,
            "userId": self.user_id,
            "username": self.user.username if self.user else None,
            "problemId": self.problem_id,
            "problemTitle": self.problem.title if self.problem else None,
            "contestId": self.contest_id,
            "language": self.language,
            "sourceCode": self.source_code,
            "status": self.status,
            "passedTests": self.passed_tests,
            "totalTests": self.total_tests,
            "runtime": f"{self.runtime_seconds:.3f}s",
            "memory": f"{self.memory_mb:.1f} MB",
            "compilerOutput": self.compiler_output,
            "testResults": results,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class Contest(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, default="")
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=90)
    problem_ids_json = Column(Text, default="[]")  # JSON list of problem IDs
    penalty_minutes_per_wrong = Column(Integer, default=10)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    submissions = relationship("Submission", back_populates="contest")
    participants = relationship("ContestParticipant", back_populates="contest", cascade="all, delete-orphan")

    def to_dict(self):
        try:
            p_ids = json.loads(self.problem_ids_json)
        except Exception:
            p_ids = []
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "startTime": self.start_time.isoformat() if self.start_time else None,
            "endTime": self.end_time.isoformat() if self.end_time else None,
            "durationMinutes": self.duration_minutes,
            "problemIds": p_ids,
            "penaltyMinutes": self.penalty_minutes_per_wrong,
            "isPublished": self.is_published,
            "participantCount": len(self.participants) if self.participants else 0,
        }


class ContestParticipant(Base):
    __tablename__ = "contest_participants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey("contests.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, default=0)
    penalty = Column(Integer, default=0)
    rank = Column(Integer, default=0)
    registered_at = Column(DateTime, default=utc_now)

    contest = relationship("Contest", back_populates="participants")
    user = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "contestId": self.contest_id,
            "userId": self.user_id,
            "username": self.user.username if self.user else "User",
            "score": self.score,
            "penalty": self.penalty,
            "rank": self.rank,
        }


class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    board_type = Column(String(32), nullable=False, index=True)  # GLOBAL, WEEKLY, MONTHLY, XP, STREAK
    snapshot_date = Column(String(32), nullable=False, index=True)
    rankings_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=utc_now)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(128), unique=True, nullable=False, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, default="")
    category = Column(String(64), default="Programming")
    difficulty = Column(String(32), default="Beginner")
    thumbnail_url = Column(String(256), default="")
    estimated_hours = Column(Float, default=10.0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")

    def to_dict(self, include_modules=False):
        data = {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "difficulty": self.difficulty,
            "thumbnailUrl": self.thumbnail_url,
            "estimatedHours": self.estimated_hours,
            "isPublished": self.is_published,
            "moduleCount": len(self.modules) if self.modules else 0,
        }
        if include_modules:
            data["modules"] = [m.to_dict(include_lessons=True) for m in self.modules]
        return data


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    order_index = Column(Integer, default=0)

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

    def to_dict(self, include_lessons=False):
        data = {
            "id": self.id,
            "courseId": self.course_id,
            "title": self.title,
            "orderIndex": self.order_index,
            "lessonCount": len(self.lessons) if self.lessons else 0,
        }
        if include_lessons:
            data["lessons"] = [l.to_dict() for l in self.lessons]
        return data


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    lesson_type = Column(String(32), default="VIDEO")  # VIDEO, PDF, ARTICLE, QUIZ, CODING
    content_url = Column(String(512), default="")
    content_text = Column(Text, default="")
    video_chapters_json = Column(Text, default="[]")
    duration_minutes = Column(Integer, default=15)
    order_index = Column(Integer, default=0)

    module = relationship("Module", back_populates="lessons")

    def to_dict(self):
        try:
            chapters = json.loads(self.video_chapters_json)
        except Exception:
            chapters = []
        return {
            "id": self.id,
            "moduleId": self.module_id,
            "title": self.title,
            "lessonType": self.lesson_type,
            "contentUrl": self.content_url,
            "contentText": self.content_text,
            "videoChapters": chapters,
            "durationMinutes": self.duration_minutes,
            "orderIndex": self.order_index,
        }


class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    score = Column(Float, default=0.0)

    user = relationship("User", back_populates="learning_progress")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    question = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON list of options
    correct_option_index = Column(Integer, nullable=False)
    explanation = Column(Text, default="")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(64), unique=True, nullable=False, index=True)
    title = Column(String(128), nullable=False)
    category = Column(String(64), nullable=False, index=True)  # Programming, Algorithms, System Design, etc.
    description = Column(Text, default="")
    icon_name = Column(String(64), default="code")
    prerequisites_json = Column(Text, default="[]")  # JSON list of skill slugs
    max_level = Column(Integer, default=5)

    def to_dict(self):
        try:
            prereqs = json.loads(self.prerequisites_json)
        except Exception:
            prereqs = []
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "iconName": self.icon_name,
            "prerequisites": prereqs,
            "maxLevel": self.max_level,
        }


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_slug = Column(String(64), nullable=False, index=True)
    current_level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="user_skills")

    def to_dict(self):
        return {
            "userId": self.user_id,
            "skillSlug": self.skill_slug,
            "level": self.current_level,
            "xp": self.xp,
        }


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, default="")
    primary_language = Column(String(32), default="python")
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="projects")
    files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")

    def to_dict(self, include_files=False):
        data = {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "description": self.description,
            "primaryLanguage": self.primary_language,
            "isPublic": self.is_public,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
            "fileCount": len(self.files) if self.files else 0,
        }
        if include_files:
            data["files"] = [f.to_dict() for f in self.files]
        return data


class ProjectFile(Base):
    __tablename__ = "project_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(256), nullable=False)
    file_path = Column(String(512), default="")
    content = Column(Text, default="")
    is_directory = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    project = relationship("Project", back_populates="files")

    def to_dict(self):
        return {
            "id": self.id,
            "projectId": self.project_id,
            "filename": self.filename,
            "filePath": self.file_path,
            "content": self.content,
            "isDirectory": self.is_directory,
        }


class AIReview(Base):
    __tablename__ = "ai_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    language = Column(String(32), nullable=False)
    source_code = Column(Text, nullable=False)
    analysis_type = Column(String(64), default="REVIEW")  # REVIEW, COMPLEXITY, TESTS, REFACTOR, HINT
    review_output = Column(Text, nullable=False)
    complexity_time = Column(String(64), default="")
    complexity_space = Column(String(64), default="")
    quality_score = Column(Integer, default=85)
    suggestions_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=utc_now)

    def to_dict(self):
        try:
            suggs = json.loads(self.suggestions_json)
        except Exception:
            suggs = []
        return {
            "id": self.id,
            "userId": self.user_id,
            "language": self.language,
            "analysisType": self.analysis_type,
            "output": self.review_output,
            "complexityTime": self.complexity_time,
            "complexitySpace": self.complexity_space,
            "qualityScore": self.quality_score,
            "suggestions": suggs,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(256), nullable=False)
    message = Column(Text, nullable=False)
    category = Column(String(64), default="SYSTEM")  # SYSTEM, CONTEST, SUBMISSION, ACHIEVEMENT, COURSE
    is_read = Column(Boolean, default=False, nullable=False)
    action_url = Column(String(256), default="")
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "message": self.message,
            "category": self.category,
            "isRead": self.is_read,
            "actionUrl": self.action_url,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, index=True)
    action = Column(String(128), nullable=False, index=True)
    resource_type = Column(String(64), nullable=False)
    resource_id = Column(String(64), nullable=True)
    ip_address = Column(String(64), nullable=True)
    status = Column(String(32), default="SUCCESS")
    details_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    def to_dict(self):
        try:
            details = json.loads(self.details_json)
        except Exception:
            details = {}
        return {
            "id": self.id,
            "userId": self.user_id,
            "action": self.action,
            "resourceType": self.resource_type,
            "resourceId": self.resource_id,
            "ipAddress": self.ip_address,
            "status": self.status,
            "details": details,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }


class RuntimeConfig(Base):
    __tablename__ = "runtime_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_id = Column(String(32), unique=True, nullable=False, index=True)
    display_name = Column(String(64), nullable=False)
    file_extension = Column(String(16), nullable=False)
    compiler_cmd = Column(String(128), default="")
    execution_cmd = Column(String(128), nullable=False)
    version_cmd = Column(String(128), default="")
    default_timeout_seconds = Column(Float, default=5.0)
    memory_limit_mb = Column(Float, default=128.0)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "languageId": self.language_id,
            "displayName": self.display_name,
            "fileExtension": self.file_extension,
            "compilerCmd": self.compiler_cmd,
            "executionCmd": self.execution_cmd,
            "versionCmd": self.version_cmd,
            "defaultTimeout": self.default_timeout_seconds,
            "memoryLimit": self.memory_limit_mb,
            "isEnabled": self.is_enabled,
        }


class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(64), nullable=False, index=True)
    username_or_email = Column(String(128), nullable=False, index=True)
    attempted_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    success = Column(Boolean, default=False, nullable=False)
    failure_reason = Column(String(128), default="")

    def to_dict(self):
        return {
            "id": self.id,
            "ipAddress": self.ip_address,
            "usernameOrEmail": self.username_or_email,
            "attemptedAt": self.attempted_at.isoformat() if self.attempted_at else None,
            "success": self.success,
            "failureReason": self.failure_reason
        }


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    theme = Column(String(32), default="dark")
    email_notifications = Column(Boolean, default=True)
    editor_font_size = Column(String(16), default="14px")
    editor_tab_size = Column(Integer, default=4)
    editor_keymap = Column(String(32), default="standard")
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="settings")

    def to_dict(self):
        return {
            "userId": self.user_id,
            "theme": self.theme,
            "emailNotifications": self.email_notifications,
            "editorFontSize": self.editor_font_size,
            "editorTabSize": self.editor_tab_size,
            "editorKeymap": self.editor_keymap,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None
        }

