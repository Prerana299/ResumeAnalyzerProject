"""
Resume parsing module.
Handles text extraction from PDF/DOCX and NLP-based entity extraction.
"""

import io
import re

import fitz  # PyMuPDF
import spacy
from docx import Document

nlp = spacy.load("en_core_web_sm")

# Skills keyword list — extend as needed
KNOWN_SKILLS = {
    "python",
    "java",
    "sql",
    "docker",
    "kubernetes",
    "git",
    "machine learning",
    "nlp",
    "streamlit",
    "fastapi",
    "flask",
    "postgresql",
    "mysql",
    "linux",
    "ci/cd",
    "github actions",
}


def extract_text(file) -> str:
    """Extract plain text from an uploaded PDF or DOCX file object."""
    filename = file.name.lower()
    raw_bytes = file.read()

    if filename.endswith(".pdf"):
        return _extract_pdf(raw_bytes)
    if filename.endswith(".docx"):
        return _extract_docx(raw_bytes)
    raise ValueError(f"Unsupported file type: {filename}")


def _extract_pdf(raw_bytes: bytes) -> str:
    text_parts = []
    with fitz.open(stream=raw_bytes, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)


def _extract_docx(raw_bytes: bytes) -> str:
    doc = Document(io.BytesIO(raw_bytes))
    return "\n".join(para.text for para in doc.paragraphs)


def parse_resume(text: str) -> dict:
    """Run NLP pipeline on extracted text and return structured data."""
    doc = nlp(text)

    name = _extract_name(doc)
    email = _extract_email(text)
    skills = _extract_skills(text)
    score = _score(skills)

    return {
        "name": name,
        "email": email,
        "skills": sorted(skills),
        "score": score,
    }


def _extract_name(doc) -> str:
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"


def _extract_email(text: str) -> str:
     match = re.search(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
     return match.group(0) if match else ""


def _extract_skills(text: str) -> list:
    lower = text.lower()
    return [skill for skill in KNOWN_SKILLS if skill in lower]


def _score(skills: list) -> int:
    """Simple percentage score: matched skills / total known skills."""
    if not KNOWN_SKILLS:
        return 0
    return round(len(skills) / len(KNOWN_SKILLS) * 100)
