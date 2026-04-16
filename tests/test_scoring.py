"""
Unit tests for role-based scoring logic in app/parser.py
Run: pytest tests/
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from parser import _score, _extract_skills, KNOWN_SKILLS


class TestScoreBoundaries:
    def test_zero_skills_gives_zero(self):
        assert _score([]) == 0

    def test_all_known_skills_gives_100(self):
        assert _score(list(KNOWN_SKILLS)) == 100

    def test_score_within_range(self):
        score = _score(["python", "sql", "docker"])
        assert 0 <= score <= 100

    def test_score_is_integer(self):
        assert isinstance(_score(["python"]), int)

    def test_single_skill_nonzero(self):
        assert _score(["python"]) > 0


class TestRoleScoring:
    """Simulate role-match scoring: how well a resume fits a role's required skills."""

    BACKEND_ROLE = {"python", "sql", "docker", "git", "linux"}
    ML_ROLE = {"python", "machine learning", "nlp", "sql"}
    DEVOPS_ROLE = {"docker", "kubernetes", "ci/cd", "git", "linux", "github actions"}

    def _role_score(self, candidate_skills: list, role_skills: set) -> int:
        """Score candidate skills against a specific role's required skills."""
        matched = [s for s in candidate_skills if s in role_skills]
        return round(len(matched) / len(role_skills) * 100)

    def test_perfect_backend_match(self):
        candidate = list(self.BACKEND_ROLE)
        assert self._role_score(candidate, self.BACKEND_ROLE) == 100

    def test_partial_backend_match(self):
        candidate = ["python", "sql"]
        score = self._role_score(candidate, self.BACKEND_ROLE)
        assert 0 < score < 100

    def test_no_match_for_role(self):
        candidate = ["streamlit", "fastapi"]
        assert self._role_score(candidate, self.ML_ROLE) == 0

    def test_ml_role_partial(self):
        candidate = ["python", "nlp"]
        score = self._role_score(candidate, self.ML_ROLE)
        assert score == 50  # 2 out of 4

    def test_devops_role_full_match(self):
        candidate = list(self.DEVOPS_ROLE)
        assert self._role_score(candidate, self.DEVOPS_ROLE) == 100

    def test_higher_skill_count_means_higher_score(self):
        one_skill = self._role_score(["python"], self.BACKEND_ROLE)
        two_skills = self._role_score(["python", "sql"], self.BACKEND_ROLE)
        assert two_skills > one_skill


class TestSkillExtractionForScoring:
    """End-to-end: extract skills from text, then score against a role."""

    def test_backend_resume_scores_nonzero(self):
        text = "Experienced with Python, SQL, Docker, Git, and Linux systems."
        skills = _extract_skills(text)
        score = _score(skills)
        assert score > 0

    def test_irrelevant_resume_scores_zero(self):
        text = "Passionate chef with expertise in French cuisine and baking."
        skills = _extract_skills(text)
        assert _score(skills) == 0

    def test_ml_resume_extracts_correctly(self):
        text = "Built NLP pipelines using Python and machine learning frameworks."
        skills = _extract_skills(text)
        assert "python" in skills
        assert "nlp" in skills
        assert "machine learning" in skills
