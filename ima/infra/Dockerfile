# ==============================
# Stage 1: Builder
# ==============================
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies (for compiling any wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install UV package manager
RUN python -m pip install --upgrade pip && pip install uv

# Copy project metadata first (leveraging Docker cache)
COPY pyproject.toml uv.lock ./

# Install only production dependencies
RUN uv sync --no-dev

# ==============================
# Stage 2: Runtime
# ==============================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy source code
COPY . .

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Ensure venv binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose application port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
