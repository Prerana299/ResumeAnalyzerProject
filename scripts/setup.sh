#!/usr/bin/env bash
# setup.sh — Bootstrap the local development environment.
set -euo pipefail

echo "==> Creating virtual environment..."
python -m venv .venv

echo "==> Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Downloading spaCy language model..."
python -m spacy download en_core_web_sm

echo ""
echo "Setup complete."
echo "  Activate env : source .venv/bin/activate"
echo "  Run app      : streamlit run app/app.py"
echo "  Run tests    : pytest tests/"
