# ========================================
# STAGE 1: Frontend Build
# ========================================
FROM node:bullseye-slim AS frontend

WORKDIR /frontend

# Install pnpm globally
RUN npm install -g pnpm

# Copy and install dependencies
COPY frontend/package.json frontend/pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile

# Copy the rest of the frontend and build
COPY frontend/ ./
RUN pnpm run build


# ========================================
# STAGE 2: Django Build & Runtime
# ========================================
FROM python:slim AS django

# Install system dependencies
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install uv
RUN pip install --no-cache-dir uv

# Copy Python dependency metadata first for caching
COPY backend/pyproject.toml /app/
COPY backend/uv.lock /app/

# Install project dependencies (without building source yet)
RUN uv sync --no-cache --locked --no-dev

# Copy project code
COPY backend /app

# Copy built frontend into Django static directory
COPY --from=frontend /frontend/dist/static/* /app/backend/static/
COPY --from=frontend /frontend/dist/index.html /app/backend/templates/index.html

# Prepare entrypoint script
ENV PATH="/app/.venv/bin:$PATH"
COPY deployment/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]