# ========================================
# STAGE 1: Frontend Build
# ========================================
FROM node:bullseye-slim AS frontend-builder

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
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install uv and update pip
RUN pip install --no-cache-dir --upgrade pip uv

# Copy Python dependency metadata first for caching
COPY backend/pyproject.toml /app/
COPY backend/uv.lock /app/

# Install project dependencies (without building source yet)
RUN uv pip install --system --no-cache .

# Copy project code
COPY backend /app

# Copy built frontend into Django static directory
# Adjust destination if your STATIC_ROOT differs
COPY --from=frontend-builder /frontend/dist /app/static/

# Prepare entrypoint script
COPY deployment/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000


# Default run command (DigitalOcean App Spec can override this)
CMD ["/app/entrypoint.sh"]