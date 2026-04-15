#!/usr/bin/env bash
# run_tests.sh — Run linting, unit tests, and (optionally) Selenium tests.
set -euo pipefail

echo "==> Lint check (flake8)..."
flake8 app/ tests/ --max-line-length=100

echo "==> Format check (black)..."
black --check app/ tests/

echo "==> Unit tests (pytest)..."
pytest tests/ -v --tb=short

if [[ "${RUN_SELENIUM:-false}" == "true" ]]; then
  echo "==> Selenium UI tests..."
  pytest selenium_tests/ -v --tb=short
else
  echo "==> Skipping Selenium tests (set RUN_SELENIUM=true to enable)."
fi

echo ""
echo "All checks passed."
