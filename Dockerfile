# Multi-stage Docker build for production optimization
FROM node:20-alpine AS frontend-builder

# Set working directory
WORKDIR /app/frontend

# Copy package files
COPY frontend/package.json frontend/yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile --production=false

# Copy frontend source
COPY frontend/ .

# Build frontend for production
RUN yarn build

# Python backend stage
FROM python:3.11-slim AS backend-builder

# Set working directory
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Production stage
FROM python:3.11-slim AS production

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy backend application
COPY --from=backend-builder /app/backend /app/backend

# Copy frontend build
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Copy configuration files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create necessary directories
RUN mkdir -p /var/log/supervisor /app/logs

# Set permissions
RUN chown -R appuser:appuser /app
RUN chmod +x /app/backend/server.py

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/api/health || exit 1

# Switch to non-root user
USER appuser

# Start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]