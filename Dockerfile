# 1. Use 3.11 to support scikit-learn 1.6.1
FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# 2. Add libxml2-dev and libxslt1-dev for lxml
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
RUN pip install --no-cache-dir -r requirements.txt

# 3. Ensure your local folder has a setup.py or pyproject.toml 
# if you keep this line. If not, delete it.
COPY . .
RUN pip install --no-cache-dir -e .

RUN mkdir -p logs artifact saved_models

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
