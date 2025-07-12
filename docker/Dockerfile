# ---------- Build Stage ----------
FROM python:3.12-slim AS builder

ARG POETRY_VERSION=2.1.1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    procps \
    git
    
RUN pip install poetry==${POETRY_VERSION} \
    && poetry config virtualenvs.create false \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction

# ---------- Runtime Stage ----------
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

COPY dagster/dagster_project /app/dagster_project

ENV PYTHONPATH=/app

CMD ["bash"]
