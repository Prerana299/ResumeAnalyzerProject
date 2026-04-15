"""
Unit tests for app/parser.py
Run: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from parser import _extract_email, _extract_skills, _score, parse_resume


class TestExtractEmail:
    def test_valid_email(self):
        assert _extract_email("contact me at john@example.com please") == "john@example.com"

    def test_no_email(self):
        assert _extract_email("no email here") == ""

    def test_email_with_subdomain(self):
        assert _extract_email("reach: user@mail.company.org") == "user@mail.company.org"


class TestExtractSkills:
    def test_known_skill_found(self):
        skills = _extract_skills("I have experience with Python and Docker.")
        assert "python" in skills
        assert "docker" in skills

    def test_case_insensitive(self):
        skills = _extract_skills("Proficient in PYTHON and SQL.")
        assert "python" in skills
        assert "sql" in skills

    def test_no_skills(self):
        skills = _extract_skills("I enjoy cooking and hiking.")
        assert skills == []


class TestScore:
    def test_empty_skills(self):
        assert _score([]) == 0

    def test_some_skills(self):
        score = _score(["python", "docker"])
        assert 0 < score <= 100

    def test_score_is_integer(self):
        assert isinstance(_score(["python"]), int)


class TestParseResume:
    SAMPLE_TEXT = """
    John Doe
    john.doe@example.com
    Skills: Python, SQL, Docker, Git
    Experience: 3 years in software development.
    """

    def test_returns_dict(self):
        result = parse_resume(self.SAMPLE_TEXT)
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = parse_resume(self.SAMPLE_TEXT)
        for key in ("name", "email", "skills", "score"):
            assert key in result

    def test_email_extracted(self):
        result = parse_resume(self.SAMPLE_TEXT)
        assert result["email"] == "john.doe@example.com"

    def test_score_range(self):
        result = parse_resume(self.SAMPLE_TEXT)
        assert 0 <= result["score"] <= 100
