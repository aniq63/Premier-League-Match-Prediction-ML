# Use 3.11 because scikit-learn 1.6.1 requires Python 3.11+
FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Install system dependencies (including lxml and git if needed)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip

# --- FIX START ---
# We remove '-e .' from requirements.txt temporarily because setup.py isn't copied yet.
# This prevents the "setup.py not found" error.
RUN sed -i '/-e \./d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt
# --- FIX END ---

# Now we copy the rest of the code (including setup.py and pyproject.toml)
COPY . .

# Now we can safely install the project itself
RUN pip install --no-cache-dir -e .

RUN mkdir -p logs artifact saved_models

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
