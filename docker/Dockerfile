# ── Build stage ─────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# FIX: ensure spaCy is available before model download
RUN /install/bin/python -m pip install spacy

# now download model
RUN /install/bin/python -m spacy download en_core_web_sm --target=/install
