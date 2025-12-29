# ============================================================================  
# DOCKERFILE FOR PREMIER LEAGUE MATCH PREDICTION ML PROJECT (Python 3.10)  
# ============================================================================  

FROM python:3.10

# ----------------------------------------------------------------------------
# ENVIRONMENT VARIABLES
# ----------------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME=/app

WORKDIR $APP_HOME

# ----------------------------------------------------------------------------
# SYSTEM DEPENDENCIES
# ----------------------------------------------------------------------------
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    python3-dev \
    libatlas-base-dev \
    gfortran \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------------
# PYTHON DEPENDENCIES
# ----------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------------
# APPLICATION CODE
# ----------------------------------------------------------------------------
COPY . .
RUN pip install --no-cache-dir -e .

# ----------------------------------------------------------------------------
# CREATE NECESSARY DIRECTORIES
# ----------------------------------------------------------------------------
RUN mkdir -p logs artifact saved_models

# ----------------------------------------------------------------------------
# NON-ROOT USER
# ----------------------------------------------------------------------------
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $APP_HOME
USER appuser

# ----------------------------------------------------------------------------
# EXPOSE PORT
# ----------------------------------------------------------------------------
EXPOSE 8000

# ----------------------------------------------------------------------------
# HEALTH CHECK
# ----------------------------------------------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# ----------------------------------------------------------------------------
# STARTUP COMMAND
# ----------------------------------------------------------------------------
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
