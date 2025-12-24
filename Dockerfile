# ============================================================================
# DOCKERFILE FOR PREMIER LEAGUE MATCH PREDICTION ML PROJECT
# ============================================================================
# This Dockerfile creates a containerized environment for the ML prediction API
# Perfect for deployment to any platform that supports Docker
# ============================================================================

# ----------------------------------------------------------------------------
# STAGE 1: BASE IMAGE
# ----------------------------------------------------------------------------
# We use Python 3.9 slim as our base image
# "slim" version is smaller than the full Python image (saves space)
# Debian-based for compatibility
FROM python:3.9-slim

# ----------------------------------------------------------------------------
# METADATA
# ----------------------------------------------------------------------------
# Add labels for documentation (who maintains this, what it does)
LABEL maintainer="aniq63"
LABEL description="Premier League Match Prediction API with FastAPI and ML"
LABEL version="1.0.0"

# ----------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# ----------------------------------------------------------------------------
# Set Python to run in unbuffered mode (logs appear immediately)
ENV PYTHONUNBUFFERED=1

# Prevent Python from writing .pyc files (compiled bytecode)
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
ENV APP_HOME=/app

# ----------------------------------------------------------------------------
# SYSTEM DEPENDENCIES
# ----------------------------------------------------------------------------
# Update package lists and install system dependencies
# - build-essential: Compiler tools needed for some Python packages
# - curl: For health checks and downloading files
# - && rm -rf /var/lib/apt/lists/*: Clean up to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------------
# WORKING DIRECTORY
# ----------------------------------------------------------------------------
# Create and set the working directory
# All subsequent commands will run from this directory
WORKDIR $APP_HOME

# ----------------------------------------------------------------------------
# PYTHON DEPENDENCIES
# ----------------------------------------------------------------------------
# Copy requirements file first (Docker layer caching optimization)
# If requirements.txt doesn't change, Docker reuses this layer
COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
# --no-cache-dir: Don't cache packages (saves space)
# --upgrade: Ensure latest compatible versions
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------------
# APPLICATION CODE
# ----------------------------------------------------------------------------
# Copy the entire application code into the container
# .dockerignore file controls what gets excluded
COPY . .

# Install the package in editable mode
# This makes the 'src' package importable
RUN pip install --no-cache-dir -e .

# ----------------------------------------------------------------------------
# CREATE NECESSARY DIRECTORIES
# ----------------------------------------------------------------------------
# Create directories that the application needs
# These might not exist in the container
RUN mkdir -p logs artifact saved_models

# ----------------------------------------------------------------------------
# PERMISSIONS
# ----------------------------------------------------------------------------
# Create a non-root user for security
# Running as root in containers is a security risk
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME

# Switch to non-root user
USER appuser

# ----------------------------------------------------------------------------
# EXPOSE PORT
# ----------------------------------------------------------------------------
# Document which port the application uses
# This doesn't actually publish the port (done with -p flag when running)
EXPOSE 8000

# ----------------------------------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------------------------------
# Docker will periodically check if the container is healthy
# Checks the /health endpoint every 30 seconds
# Waits 30s before first check, times out after 10s, retries 3 times
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ----------------------------------------------------------------------------
# STARTUP COMMAND
# ----------------------------------------------------------------------------
# This command runs when the container starts
# uvicorn: ASGI server for FastAPI
# app:app: module:application (app.py file, app variable)
# --host 0.0.0.0: Listen on all network interfaces (accessible from outside)
# --port 8000: Port to run on
# --workers 1: Number of worker processes (increase for production)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# ============================================================================
# BUILD INSTRUCTIONS:
# docker build -t epl-prediction:latest .
#
# RUN INSTRUCTIONS:
# docker run -p 8000:8000 epl-prediction:latest
#
# ACCESS:
# http://localhost:8000
# ============================================================================
