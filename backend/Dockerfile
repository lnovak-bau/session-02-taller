# --- Build stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy dependency files first for layer caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies into a virtual environment inside the project
RUN poetry config virtualenvs.in-project true \
    && poetry install --only main --no-interaction --no-ansi

# --- Runtime stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv .venv

# Copy application source
COPY app ./app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
