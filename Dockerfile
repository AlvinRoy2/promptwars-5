# ==============================================================================
# Multi-Stage Dockerfile for Event Architecture & Production Studio
#
# Stage 1: Build production React + Tailwind CSS frontend bundle
# Stage 2: Minimal, secure Python 3.12 runtime serving both FastAPI & React SPA
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Frontend Builder
# ------------------------------------------------------------------------------
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

# Leverage Docker layer caching for dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy frontend source files
COPY frontend/ ./

# Optional build-time argument to override API URL (defaults to auto-detecting current origin)
ARG VITE_API_URL=""
ENV VITE_API_URL=${VITE_API_URL}

# Compile static bundle to /app/frontend/dist
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 2: Production Python Runtime
# ------------------------------------------------------------------------------
FROM python:3.12-slim AS runner

# Container labels
LABEL maintainer="Promptwars Production Engineering"
LABEL description="Event Architecture & Production Studio Unified Container"

# Configure Python execution flags for containers
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HOST=0.0.0.0 \
    PORT=8000

# Install curl for healthcheck validation and cleanup in single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root system user and group (Principle of Least Privilege)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app

# Install Python backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Copy backend application source
COPY backend/ ./backend/

# Copy compiled frontend SPA from builder stage
# Placed in both /app/frontend/dist and /app/backend/static to guarantee resolution
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./backend/static

# Grant ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root execution context
USER appuser

# Expose target listening port
EXPOSE 8000

# Native container healthcheck endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Launch production server with dynamic port support (compatible with Cloud Run, Railway, Render, Docker Compose)
CMD ["sh", "-c", "exec uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
