"""Shared helper functions for the resume analyzer app."""

from collections.abc import Iterable


def normalize_text(text: str) -> str:
    """Collapse repeated whitespace and trim surrounding space."""
    return " ".join(text.split())


def format_skills(skills: Iterable[str]) -> str:
    """Return a readable comma-separated skill list."""
    cleaned = [skill.strip() for skill in skills if skill and skill.strip()]
    return ", ".join(sorted(cleaned))


def clamp_score(score: int, minimum: int = 0, maximum: int = 100) -> int:
    """Keep a score within the expected percentage range."""
    return max(minimum, min(maximum, score))
