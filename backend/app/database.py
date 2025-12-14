"""
Database Configuration
PostgreSQL connection settings using SQLAlchemy
"""

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# =============================================================================
# Load environment variables from .env file
# =============================================================================

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/betashift"  # default fallback
)


# =============================================================================
# SQLAlchemy Engine
# =============================================================================

engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL logging (set to False in production)
    pool_pre_ping=True,  # Check connection health before using
)


# =============================================================================
# Session Factory
# =============================================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =============================================================================
# Base Class for Models
# =============================================================================

Base = declarative_base()


# =============================================================================
# Dependency for FastAPI
# =============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI endpoints.

    Usage in routers:
        @router.get("/")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    - Creates a new session for each request
    - Automatically closes the session after request completes
    - Handles cleanup even if an error occurs
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
