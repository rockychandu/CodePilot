"""
CodePilot Database Connection & Session Management
Supports SQLite for zero-config development and PostgreSQL for enterprise production.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///codepilot.db")

# SQLite connection args for multi-threaded access
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Create all database tables."""
    from codepilot.db import models  # noqa: F401
    Base.metadata.create_all(bind=engine)


def get_db():
    """Contextual database session provider."""
    db = db_session()
    try:
        yield db
    finally:
        db.close()
