"""
Unit tests for app/database.py
Uses an in-memory SQLite database to avoid side effects.
Run: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import pytest
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import database as db


@pytest.fixture(autouse=True)
def fresh_db():
    """Recreate tables before each test."""
    db.Base.metadata.drop_all(bind=db.engine)
    db.init_db()


class TestInitDb:
    def test_tables_created(self):
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        assert "resume_results" in inspector.get_table_names()


class TestSaveResult:
    def test_save_and_retrieve(self):
        payload = {"name": "Alice", "email": "alice@test.com", "skills": ["python"], "score": 50}
        db.save_result(payload)
        results = db.get_all_results()
        assert len(results) == 1
        assert results[0]["name"] == "Alice"
        assert results[0]["score"] == 50

    def test_multiple_saves(self):
        db.save_result({"name": "A", "email": "", "skills": [], "score": 0})
        db.save_result({"name": "B", "email": "", "skills": [], "score": 10})
        assert len(db.get_all_results()) == 2

    def test_skills_stored_as_string(self):
        db.save_result({"name": "X", "email": "", "skills": ["python", "sql"], "score": 20})
        result = db.get_all_results()[0]
        assert "python" in result["skills"]
        assert "sql" in result["skills"]
