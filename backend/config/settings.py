"""
CodePilot Enterprise Configuration System
Defines environment variables, runtime settings, sandbox limits, security policies, and defaults.
"""

import os
from typing import Dict, Any

class Settings:
    # Environment
    ENV: str = os.environ.get("ENV", "production")
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", 5000))
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "codepilot-super-secure-production-secret-key-2026")
    
    # Database
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///codepilot.db")
    DB_POOL_SIZE: int = int(os.environ.get("DB_POOL_SIZE", 20))
    DB_MAX_OVERFLOW: int = int(os.environ.get("DB_MAX_OVERFLOW", 30))
    
    # Auth & Security
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "codepilot-jwt-token-signing-key-998244353")
    JWT_EXPIRATION_HOURS: int = int(os.environ.get("JWT_EXPIRATION_HOURS", 24))
    REFRESH_TOKEN_EXPIRATION_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRATION_DAYS", 30))
    PASSWORD_SALT_ROUNDS: int = 100000
    RATE_LIMIT_PER_MINUTE: int = int(os.environ.get("RATE_LIMIT_PER_MINUTE", 120))
    
    # Execution Sandbox Resource Limits
    DEFAULT_EXECUTION_TIMEOUT_SECONDS: float = float(os.environ.get("EXEC_TIMEOUT", 5.0))
    MAX_EXECUTION_TIMEOUT_SECONDS: float = 15.0
    DEFAULT_MEMORY_LIMIT_MB: float = float(os.environ.get("EXEC_MEMORY_MB", 128.0))
    MAX_MEMORY_LIMIT_MB: float = 512.0
    MAX_SOURCE_CODE_BYTES: int = 1024 * 1024  # 1 MB
    MAX_OUTPUT_BYTES: int = 512 * 1024  # 512 KB
    
    # Contest & Judge Settings
    JUDGE_PARALLEL_WORKERS: int = int(os.environ.get("JUDGE_WORKERS", 4))
    CONTEST_PENALTY_MINUTES: int = 10
    
    # Pilot AI Engine
    AI_MAX_CONTEXT_TOKENS: int = 8192
    AI_REQUEST_TIMEOUT_SECONDS: int = 10
    
    # Storage & Workspace
    PROJECT_STORAGE_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage", "workspaces"))
    MAX_PROJECT_FILES_PER_USER: int = 200
    MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

settings = Settings()
