# ============================================
# Customer Churn Prediction - Production Dockerfile
# Stage 10: Containerization & Cloud Deployment
# ============================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files & enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first for efficient Docker layer caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and models
COPY backend/ ./backend/
COPY models/ ./models/
COPY tests/ ./tests/

# Expose port 8000 for FastAPI
EXPOSE 8000

# Health check endpoint verification
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start production uvicorn web server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
