# Enterprise MLOps Churn Prediction Platform

A production-style, Amazon-like Customer Churn Prediction Platform built to teach
enterprise MLOps practices: modular ML pipelines, experiment tracking with MLflow,
containerization with Podman/Docker, and deployment to Kubernetes.

## Architecture / Development Flow

```
VS Code
   ↓
GitHub
   ↓
Python Development
   ↓
MLflow
   ↓
Podman Build
   ↓
Podman Run
   ↓
Local API Testing
   ↓
Podman Desktop (Optional)
   ↓
Kubernetes (Kind or Minikube)
   ↓
GKE
```

## Project Structure

```
enterprise-mlops-churn/
├── data/               # raw + processed datasets, sample payloads
├── notebooks/          # exploratory analysis notebooks
├── src/                # core ML pipeline modules
├── api/                # FastAPI serving layer
├── model/              # serialized model + scaler artifacts
├── artifacts/          # metrics, plots, evaluation outputs
├── mlruns/             # MLflow tracking store (local)
├── tests/              # unit tests
├── kubernetes/         # k8s manifests (Deployment/Service/Ingress/KServe)
├── config/             # YAML configuration (app, logging, model)
├── .github/workflows/  # CI pipeline
├── Dockerfile / Containerfile
└── docker-compose.yml
```

## Quickstart (local, Python)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Train the model (runs ingestion -> preprocessing -> feature engineering -> train -> evaluate)
python -m src.train

# 2. Run the API
uvicorn api.app:app --reload --port 8000

# 3. Test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @data/sample_prediction.json
```

## Quickstart (Podman)

```bash
podman build -t churn-api:latest -f Containerfile .
podman run -p 8000:8000 churn-api:latest
```

Docker works identically, substituting `docker` for `podman` and `Dockerfile` for `Containerfile`.

## Quickstart (Kubernetes - Kind/Minikube)

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

## MLflow Tracking

```bash
mlflow ui --backend-store-uri ./mlruns
# open http://localhost:5000
```

## Endpoints

| Method | Path       | Description                          |
|--------|-----------|---------------------------------------|
| GET    | `/`       | Root / service info                   |
| GET    | `/health` | Health check for k8s liveness probes  |
| POST   | `/predict`| Predict churn probability for a customer |
| GET    | `/metrics`| Latest stored model evaluation metrics|

## License
See `LICENSE`.
