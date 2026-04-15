# Smart Resume Analyzer

A DevOps mini project that uses Python, Streamlit, and NLP to automatically parse resumes, extract structured insights, and persist results to a database — giving recruiters and candidates actionable feedback through a clean web interface.

---

## Problem Statement

Recruiters spend an average of six seconds skimming a resume before deciding whether to continue reading. This manual, error-prone process fails both sides: strong candidates are overlooked because their resumes are poorly formatted, and hiring managers waste time on applicants who clearly lack required skills.

There is no lightweight, self-hosted tool that can:
- parse a raw resume (PDF/DOCX) without relying on paid third-party APIs,
- extract structured entities (skills, education, experience) using NLP,
- score the resume against a target role, and
- store historical results so trends can be analyzed over time.

**Smart Resume Analyzer** fills that gap.

---

## Project Objectives

| # | Objective |
|---|-----------|
| 1 | Accept resume uploads in PDF and DOCX formats through a browser-based UI. |
| 2 | Extract key entities — name, contact info, skills, education, and work experience — using NLP (spaCy / NLTK). |
| 3 | Score each resume against a configurable job-role profile and highlight missing skills. |
| 4 | Persist parsed results and scores in a relational database for audit and reporting. |
| 5 | Display an interactive dashboard (Streamlit) with per-resume feedback and aggregate analytics. |
| 6 | Package the entire stack with Docker and automate CI/CD via GitHub Actions. |

---

## System Workflow

```
User uploads resume (PDF / DOCX)
        │
        ▼
┌─────────────────────┐
│  Streamlit Frontend  │  ← browser-based, port 8501
└────────┬────────────┘
         │ raw file bytes
         ▼
┌─────────────────────┐
│   File Parser        │  ← PyMuPDF (PDF) / python-docx (DOCX)
│   (text extraction)  │
└────────┬────────────┘
         │ plain text
         ▼
┌─────────────────────┐
│   NLP Pipeline       │  ← spaCy NER + custom skill matcher
│   Entity extraction  │     outputs: name, skills[], edu[], exp[]
└────────┬────────────┘
         │ structured JSON
         ▼
┌─────────────────────┐
│   Scoring Engine     │  ← compares extracted skills vs. job profile
│                      │     outputs: match %, missing skills, suggestions
└────────┬────────────┘
         │ results
         ▼
┌─────────────────────┐
│   Database Layer     │  ← SQLite (dev) / PostgreSQL (prod)
│   (SQLAlchemy ORM)   │     stores: resume metadata, scores, timestamps
└────────┬────────────┘
         │ query results
         ▼
┌─────────────────────┐
│  Dashboard / Report  │  ← Streamlit charts, per-upload feedback panel
└─────────────────────┘
```

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                     Docker Compose                        │
│                                                           │
│  ┌─────────────────────┐    ┌──────────────────────────┐ │
│  │   app  (container)   │    │   db   (container)        │ │
│  │                      │    │                          │ │
│  │  Streamlit :8501     │◄──►│  PostgreSQL :5432        │ │
│  │  ├── file_parser.py  │    │  (volume: pgdata)        │ │
│  │  ├── nlp_engine.py   │    └──────────────────────────┘ │
│  │  ├── scorer.py       │                                  │
│  │  └── db/models.py    │                                  │
│  └─────────────────────┘                                  │
│                                                           │
└──────────────────────────────────────────────────────────┘

CI/CD  →  GitHub Actions
           ├── lint (flake8, black)
           ├── test (pytest)
           └── build & push Docker image
```

**Key technology choices:**

| Layer | Technology | Reason |
|-------|-----------|--------|
| UI | Streamlit | Rapid prototyping; no separate frontend build step |
| NLP | spaCy + NLTK | Mature, offline, extensible entity recognition |
| File parsing | PyMuPDF, python-docx | Handles both PDF and DOCX without Office dependency |
| ORM | SQLAlchemy | Database-agnostic; easy migration from SQLite → PostgreSQL |
| Database | SQLite (dev) / PostgreSQL (prod) | Zero-config locally; production-grade in containers |
| Containerization | Docker + Docker Compose | Reproducible environment across team members |
| CI/CD | GitHub Actions | Native to the repo; free for public projects |

---

## Repository Structure (planned)

```
ResumeAnalyzerProject/
├── app/
│   ├── main.py              # Streamlit entry point
│   ├── file_parser.py       # PDF / DOCX text extraction
│   ├── nlp_engine.py        # spaCy NER & skill matching
│   ├── scorer.py            # Resume scoring logic
│   └── db/
│       ├── models.py        # SQLAlchemy models
│       └── session.py       # DB connection management
├── job_profiles/            # YAML files defining role skill sets
├── tests/                   # pytest test suite
├── .github/workflows/       # GitHub Actions CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd ResumeAnalyzerProject

# 2. (Option A) Run locally with a virtual environment
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py

# 3. (Option B) Run with Docker Compose
docker compose up --build
# then open http://localhost:8501
```

---

## Team

All development happens on feature branches. `main` is the integration branch — no direct commits.

| Member | Branch |
|--------|--------|
| Mayur | `mayuri` |
| Anushka | `anushka` |
| Prerana | `prerana` |
| Sejal | `sejal` |
