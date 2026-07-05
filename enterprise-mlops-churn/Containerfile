# Standard Dockerfile - works with docker build / podman build
FROM python:3.11-slim

WORKDIR /app

# System deps for xgboost / matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Train the model at build time so the image is self-contained.
# In production this step is typically skipped in favor of pulling a
# model artifact from a registry (MLflow Model Registry / GCS / S3).
RUN python -m src.train

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
