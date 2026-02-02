# Multi-stage Dockerfile for React Frontend + FastAPI Backend

# ============================================
# Stage 1: Build React Frontend
# ============================================
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

# Copy package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build React app for production
RUN npm run build

# ============================================
# Stage 2: Python Backend + Serve React
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Install essential system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libglib2.0-0 \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*


# Upgrade pip, setuptools, wheel, and regex
RUN pip install --upgrade pip setuptools wheel regex --no-cache-dir

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy backend source code
COPY backend/ /app/backend/
COPY patterns/ /app/patterns/
COPY utils/ /app/utils/

# Copy React build from frontend-builder stage
COPY --from=frontend-builder /frontend/build /app/frontend/build

# Expose port for FastAPI (React will be served through FastAPI)
EXPOSE 8602

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV REACT_APP_API_URL=""

# Start FastAPI server (which will also serve React static files)
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8602"]
