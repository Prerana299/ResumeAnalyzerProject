# ── Build stage ─────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# spaCy model install (safe in build stage)
RUN python -m spacy download en_core_web_sm --target=/install


# ── Runtime stage ───────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install curl (for healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy full project
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Healthcheck for Streamlit
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ── FIXED ENTRYPOINT (correct format) ──
ENTRYPOINT ["streamlit", "run", "app/app.py"]

# Runtime arguments (clean separation)
CMD ["--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
