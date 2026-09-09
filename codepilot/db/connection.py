"""
CodePilot Database Connection & Session Management
Supports SQLite for zero-config development and PostgreSQL for enterprise production.
"""

import os
from sqlalchemy import create_engine, text
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
    """Create all database tables and perform lightweight schema migrations."""
    from codepilot.db import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Lightweight SQLite column migrations for smooth upgrades
    if DATABASE_URL.startswith("sqlite"):
        with engine.connect() as conn:
            try:
                # Check users table columns
                res = conn.execute(text("PRAGMA table_info(users);")).fetchall()
                col_names = [r[1] for r in res]
                if "last_login_at" not in col_names and "users" in [t[0] for t in conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()]:
                    conn.execute(text("ALTER TABLE users ADD COLUMN last_login_at DATETIME;"))
                    conn.commit()
            except Exception:
                pass


from contextlib import contextmanager

@contextmanager
def get_db_session():
    """Context manager for database sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db():
    """Contextual database session provider."""
    db = db_session()
    try:
        yield db
    finally:
        db.close()
