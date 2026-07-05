# Enterprise MLOps Platform — Project Overview
### Enterprise E-Commerce Customer Churn Prediction Platform

*A team demonstration document — what's built, how it fits together, and what's next.*

---

## 1. What This Project Is

A production-style customer churn prediction platform built to demonstrate a
complete enterprise MLOps workflow — from raw customer data to a monitored,
auto-scaling prediction API running on Kubernetes.

The project also doubles as the backbone of a 45-day Enterprise MLOps
training course: every module in the course maps to a working piece of this
same system, so the demo below is simultaneously the curriculum's capstone.

---

## 2. End-to-End Architecture Flow

```
Customer Data (PostgreSQL / RDS)
      │
      ▼
Data Validation  ──────────────►  src/data_ingestion.py
      │
      ▼
Data Cleaning & Encoding  ─────►  src/preprocessing.py
      │
      ▼
Feature Engineering  ──────────►  src/feature_engineering.py
      │
      ▼
Model Training (RF + XGBoost)  ►  src/train.py
      │
      ▼
Experiment Tracking  ──────────►  MLflow
      │
      ▼
Model Evaluation  ─────────────►  src/evaluate.py
      │
      ▼
Best Model Selected & Saved  ──►  model/customer_churn.pkl
      │
      ▼
REST API (FastAPI)  ───────────►  api/app.py
      │
      ▼
Containerized  ────────────────►  Dockerfile / Containerfile
      │
      ▼
CI Pipeline  ───────────────────►  GitHub Actions
      │
      ▼
Deployed to Kubernetes  ───────►  kubernetes/deployment.yaml, service.yaml, ingress.yaml
      │
      ▼
Serving Layer  ─────────────────►  FastAPI (live today) / KServe (built, planned)
      │
      ▼
Monitoring  ─────────────────────►  Prometheus + Grafana (planned)
      │
      ▼
Drift Detection & Retraining  ──►  (planned)
```

**Status legend for the diagram above:** everything through "Deployed to
Kubernetes" and the FastAPI serving path is built and demonstrable today.
KServe, Prometheus/Grafana, and automated retraining are designed
(manifests/plans exist) but not yet live — see Section 6.

---

## 3. What the Team Can See Working Today

### 3.1 Data Layer
- PostgreSQL database (`ml_ops_db`) with a least-privilege application user (`ml_user`)
- 1,000 seeded customer records (synthetic Indian-market data) in `churn.customers`
- A parallel CSV dataset (`data/raw/customer_churn.csv`) the current pipeline reads from

### 3.2 ML Pipeline
- Ingestion → cleaning → encoding → feature engineering, each as its own tested module
- Two models trained side by side (Random Forest, XGBoost); best one selected automatically by ROC-AUC
- Evaluation artifacts generated automatically: metrics.json, confusion matrix, feature importance

### 3.3 Serving
- FastAPI service with four endpoints: `/`, `/health`, `/predict`, `/metrics`
- Auto-generated Swagger docs at `/docs`
- Input validation via Pydantic — bad requests are rejected with clear errors

### 3.4 Packaging & Deployment
- Docker and Podman both supported from the same image definitions
- Kubernetes manifests for Deployment, Service, and Ingress, with health probes and resource limits already configured
- GitHub Actions CI: every push trains the model, runs the test suite, and builds the image

### 3.5 Testing
- 11 automated tests covering data validation, preprocessing, prediction correctness, and all API endpoints

---

## 4. Live Demo Flow (Suggested Script)

Use this sequence when presenting to the team — each step takes under a minute and shows a different layer of the stack.

```
1. Show the database
   psql -h <host> -U ml_user -d ml_ops_db -c "SELECT count(*) FROM churn.customers;"

2. Run the training pipeline
   python -m src.train
   → walk through the console output: ingestion → preprocessing → training → best model selected

3. Open the MLflow UI
   mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
   → compare the Random Forest vs XGBoost runs side by side

4. Start the API
   uvicorn api.app:app --reload --port 8000
   → open http://localhost:8000/docs and run a live prediction from the Swagger UI

5. Show the container build
   podman build -t churn-api:latest -f Containerfile .
   podman run -p 8000:8000 churn-api:latest
   → same API, now fully containerized

6. Show it running on Kubernetes
   kubectl apply -f kubernetes/deployment.yaml -f kubernetes/service.yaml -f kubernetes/ingress.yaml
   kubectl get pods
   → point out replica count, health checks, resource limits

7. Show the CI pipeline
   → open the GitHub Actions tab, point at the last run: train → test → build
```

---

## 5. Technology Stack

| Layer | Tools |
|---|---|
| Data | PostgreSQL (Amazon RDS-compatible) |
| ML | scikit-learn, XGBoost, pandas, NumPy |
| Experiment Tracking | MLflow |
| Serving | FastAPI, Uvicorn |
| Containerization | Docker, Podman |
| Orchestration | Kubernetes (Kind/Minikube locally, GKE for production) |
| CI/CD | GitHub Actions (Cloud Build + Argo CD planned) |
| Testing | pytest |
| Planned | KServe, Kubeflow, AWS SageMaker, Prometheus, Grafana |

---

## 6. What's Built vs. What's Planned

| Capability | Status |
|---|---|
| Data validation, cleaning, feature engineering | ✅ Working |
| Model training + evaluation | ✅ Working |
| Experiment tracking (MLflow, SQLite backend) | ✅ Working |
| REST API with validation | ✅ Working |
| Docker/Podman containerization | ✅ Working |
| Kubernetes deployment (Deployment/Service/Ingress) | ✅ Working |
| CI pipeline (train, test, build) | ✅ Working |
| Data versioning (DVC + S3) | 🟡 Config in place, remote not connected |
| MLflow Model Registry (PostgreSQL backend) | 🟡 Currently SQLite, upgrade planned |
| KServe model serving | 🟡 Manifest written, not yet deployed live |
| Full CI/CD with Argo CD (GitOps) | 🟡 GitHub Actions works, GitOps layer planned |
| Kubeflow pipeline automation | ⬜ Planned |
| AWS SageMaker training/deployment path | ⬜ Planned |
| Prometheus + Grafana monitoring | ⬜ Planned |
| Data/model drift detection & auto-retraining | ⬜ Planned |
| RBAC, Secrets management, multi-environment configs | ⬜ Planned |

---

## 7. Why This Matters for the Team

- **Reproducibility:** every model run is tracked, every environment is defined in code (Docker, Kubernetes manifests) — no "works on my machine."
- **Speed to production:** a new model version can go from `python -m src.train` to a running Kubernetes pod in minutes, not days.
- **Auditability:** MLflow keeps a full history of every experiment's parameters, metrics, and artifacts.
- **Extensibility:** the roadmap items (KServe, SageMaker, monitoring) plug into the existing pipeline without rearchitecting anything already built.

---

## 8. Recommended Next Steps

1. Wire the ML pipeline to read from PostgreSQL instead of the static CSV, so the data layer and model layer are fully connected.
2. Move MLflow's backend from SQLite to PostgreSQL and enable the Model Registry for proper staging → production promotion.
3. Stand up Prometheus + Grafana for basic API and model-health monitoring — the fastest win for production confidence.
4. Extend the CI pipeline to push images to a registry and deploy via GitOps (Argo CD), closing the loop from commit to production.
