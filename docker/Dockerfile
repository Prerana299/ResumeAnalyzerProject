# ── Build stage ─────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

# install everything into SAME environment (IMPORTANT FIX)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# install spaCy into same prefix
RUN pip install --no-cache-dir --prefix=/install spacy

# use correct python from install prefix
RUN /install/bin/python -m spacy download en_core_web_sm

# install spaCy in same environment
RUN pip install --no-cache-dir --prefix=/install spacy

# set PATH so installed python/packages are visible
ENV PATH="/install/bin:$PATH"

# download model
RUN python -m spacy download en_core_web_sm


# ── Runtime stage ───────────────────────────
FROM python:3.11-slim

WORKDIR /app

# install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# copy installed packages
COPY --from=builder /install /usr/local

# copy project
COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# correct Streamlit entrypoint
ENTRYPOINT ["streamlit", "run", "app/app.py"]

CMD ["--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
