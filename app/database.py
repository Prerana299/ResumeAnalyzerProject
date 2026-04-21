"""
Database layer — SQLite (dev) / PostgreSQL (prod) via SQLAlchemy.
"""

import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./resume_analyzer.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


# class Base(DeclarativeBase):
#     pass


class ResumeResult(Base):
    __tablename__ = "resume_results"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    email = Column(String(200))
    skills = Column(Text)  # comma-separated list
    score = Column(Integer)
    analyzed_at = Column(DateTime, default=datetime.utcnow)


def init_db() -> None:
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def save_result(result: dict) -> None:
    """Persist a parsed resume result to the database."""
    with Session(engine) as session:
        record = ResumeResult(
            name=result.get("name", ""),
            email=result.get("email", ""),
            skills=", ".join(result.get("skills", [])),
            score=result.get("score", 0),
        )
        session.add(record)
        session.commit()


def get_all_results() -> list[dict]:
    """Return all stored results as a list of dicts."""
    with Session(engine) as session:
        rows = (
            session.query(ResumeResult).order_by(ResumeResult.analyzed_at.desc()).all()
        )
        return [
            {
                "id": r.id,
                "name": r.name,
                "email": r.email,
                "skills": r.skills,
                "score": r.score,
                "analyzed_at": str(r.analyzed_at),
            }
            for r in rows
        ]
