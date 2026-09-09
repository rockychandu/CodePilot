"""
CodePilot Data Validation & Serialization Schemas
Type-safe Pydantic models for REST endpoints and internal contracts.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr

# -------------------------------------------------------------------
# Auth & User Schemas
# -------------------------------------------------------------------
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=120)
    password: str = Field(..., min_length=6, max_length=128)
    displayName: Optional[str] = Field(None, max_length=100)

class UserLoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    loginIdentifier: Optional[str] = None
    password: str

class TokenRefreshRequest(BaseModel):
    refreshToken: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetConfirmRequest(BaseModel):
    token: str
    password: str = Field(..., min_length=6, max_length=128)

class ProfileUpdateRequest(BaseModel):
    displayName: Optional[str] = None
    bio: Optional[str] = None
    primaryLanguage: Optional[str] = None
    preferredLanguages: Optional[List[str]] = None
    avatarUrl: Optional[str] = None

# -------------------------------------------------------------------
# Code Execution & Runtime Schemas
# -------------------------------------------------------------------
class CodeExecutionRequest(BaseModel):
    language: str = Field(..., min_length=1, max_length=32)
    sourceCode: Optional[str] = None
    code: Optional[str] = None
    stdin: Optional[str] = ""
    timeout: Optional[float] = 5.0
    memoryLimit: Optional[float] = 128.0

class CodeExecutionResponse(BaseModel):
    status: str
    stdout: str
    stderr: str
    output: str
    exitCode: int
    runtime: str
    runtimeSeconds: float
    memory: str
    memoryMb: float

class RuntimeSmokeTestResponse(BaseModel):
    language: str
    displayName: str
    installed: bool
    status: str
    version: str
    testPassed: bool
    output: str

# -------------------------------------------------------------------
# Competitive Programming & Judge Schemas
# -------------------------------------------------------------------
class ProblemCreateRequest(BaseModel):
    slug: str
    title: str
    difficulty: str  # Easy, Medium, Hard
    category: str
    description: str
    constraints: Optional[str] = ""
    tags: Optional[List[str]] = []
    starterTemplates: Optional[Dict[str, str]] = {}
    timeLimit: Optional[float] = 2.0
    memoryLimit: Optional[float] = 128.0

class SubmissionCreateRequest(BaseModel):
    problemId: int
    language: str
    sourceCode: str
    contestId: Optional[int] = None

class SubmissionResultResponse(BaseModel):
    submissionId: int
    status: str  # Accepted, Wrong Answer, Compilation Error, Runtime Error, Time Limit Exceeded
    passedTests: int
    totalTests: int
    runtime: str
    memory: str
    compilerOutput: Optional[str] = ""
    testResults: List[Dict[str, Any]] = []

# -------------------------------------------------------------------
# Contest Schemas
# -------------------------------------------------------------------
class ContestCreateRequest(BaseModel):
    slug: str
    title: str
    description: Optional[str] = ""
    startTime: str
    endTime: str
    durationMinutes: Optional[int] = 90
    problemIds: Optional[List[int]] = []
    penaltyMinutes: Optional[int] = 10

# -------------------------------------------------------------------
# Project Workspace Schemas
# -------------------------------------------------------------------
class ProjectCreateRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    language: Optional[str] = "python"
    template: Optional[str] = "basic"

class ProjectFileUpdateRequest(BaseModel):
    filename: str
    content: str
    filePath: Optional[str] = ""

# -------------------------------------------------------------------
# Pilot AI Assistant Schemas
# -------------------------------------------------------------------
class AIReviewRequest(BaseModel):
    language: str
    sourceCode: str

class AIComplexityRequest(BaseModel):
    language: str
    sourceCode: str

class AIGenerateTestsRequest(BaseModel):
    language: str
    sourceCode: str

class AIExplainBugRequest(BaseModel):
    language: str
    sourceCode: str
    errorMessage: Optional[str] = ""

# -------------------------------------------------------------------
# Admin Schemas
# -------------------------------------------------------------------
class RoleUpdateRequest(BaseModel):
    role: str  # USER, MODERATOR, INSTRUCTOR, ADMIN
