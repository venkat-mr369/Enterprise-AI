# RUNBOOK — Enterprise Customer Churn Prediction Platform

Operational guide for taking this project from a fresh clone to a running
Kubernetes deployment. Follow the steps in order the first time; after that,
jump to whichever section you need.

---

## Flow at a Glance

```
Extract / Clone
      ↓
venv + pip install
      ↓
python -m src.train   (ingestion → preprocessing → features → train → evaluate)
      ↓
mlflow ui              (compare runs)
      ↓
uvicorn api.app:app    (local API test)
      ↓
pytest tests/          (validate)
      ↓
podman/docker build + run   (containerize)
      ↓
kind/minikube + kubectl apply   (local k8s)
      ↓
GKE push + deploy       (production)
```

---

## Step 1 — Extract and Set Up the Environment

```bash
# 1a. Unzip (skip if you cloned from GitHub instead)
unzip enterprise-mlops-churn.zip
cd enterprise-mlops-churn

# 1b. Create an isolated Python environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 1c. Install dependencies
pip install -r requirements.txt
```

**Verify:**
```bash
python -c "import fastapi, sklearn, xgboost, mlflow; print('ok')"
```
Expected output: `ok`

---

## Step 2 — Run the Training Pipeline

```bash
python -m src.train
```

### What happens under the hood

```
src/data_ingestion.py        → loads data/raw/customer_churn.csv, validates schema
        ↓
src/preprocessing.py         → cleans nulls, encodes categoricals
        ↓
src/feature_engineering.py   → adds CLV, AvgMonthlySpend, TenureYears
        ↓                       saves data/processed/customer_churn_processed.csv
src/train.py                 → trains RandomForest + XGBoost, logs both to MLflow
        ↓
src/evaluate.py              → computes Accuracy / Precision / Recall / F1 / ROC-AUC
        ↓
        picks best model by ROC-AUC
              → saves model/customer_churn.pkl
              → saves model/scaler.pkl, model/feature_columns.pkl
              → saves artifacts/metrics.json, confusion_matrix.png, feature_importance.csv
```

**Verify:**
```bash
ls model/            # customer_churn.pkl, scaler.pkl, feature_columns.pkl
cat artifacts/metrics.json
```

**Troubleshooting**
| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: data/raw/customer_churn.csv` | Running from wrong directory | `cd` into the project root before running |
| `MlflowException: filesystem tracking backend ... maintenance mode` | Newer MLflow requires a database backend | Already configured to use `sqlite:///mlruns/mlflow.db` in `config/config.yaml` — confirm that value wasn't changed |
| `ModuleNotFoundError: No module named 'src'` | Not running as a module | Use `python -m src.train`, not `python src/train.py` |

---

## Step 3 — Inspect Results with MLflow

```bash
mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
```
Open **http://localhost:5000** and compare the `random_forest` vs `xgboost` runs — parameters, metrics, and logged model artifacts side by side.

---

## Step 4 — Run and Test the API Locally

```bash
uvicorn api.app:app --reload --port 8000
```

In a second terminal:

```bash
curl http://localhost:8000/health

curl http://localhost:8000/metrics

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @data/sample_prediction.json
```

**Expected `/health` response:**
```json
{"status": "healthy", "model_loaded": true}
```

If `model_loaded` is `false`, re-run Step 2 — the API can't find `model/customer_churn.pkl`.

---

## Step 5 — Run the Test Suite

```bash
pytest tests/ -v
```

Covers: data ingestion, preprocessing, feature engineering, prediction correctness, and all API endpoints (11 tests total). Run this after any code change before rebuilding the container.

---

## Step 6 — Build and Run the Container (Podman)

```bash
podman build -t churn-api:latest -f Containerfile .
podman run -p 8000:8000 churn-api:latest
```

Docker works identically — swap `podman` → `docker` and `Containerfile` → `Dockerfile`.

**Run API + MLflow UI together:**
```bash
podman compose up      # or: docker compose up
```

**Verify:**
```bash
curl http://localhost:8000/health
```

> Note: the image trains the model at build time (`RUN python -m src.train` inside the Dockerfile), so the container is self-contained — no need to mount a pre-trained model for local testing.

---

## Step 7 — Deploy to Local Kubernetes (Kind or Minikube)

```bash
# 7a. Start a local cluster
kind create cluster --name churn-cluster     # or: minikube start

# 7b. Load the image into the cluster
kind load docker-image churn-api:latest --name churn-cluster
# Minikube alternative:
#   eval $(minikube docker-env)
#   docker build -t churn-api:latest -f Containerfile .

# 7c. Apply manifests
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

# 7d. Verify
kubectl get pods
kubectl get svc
kubectl port-forward svc/churn-api-service 8000:80
curl http://localhost:8000/health
```

**Troubleshooting**
| Symptom | Cause | Fix |
|---|---|---|
| Pod stuck in `ImagePullBackOff` | Image not loaded into cluster | Re-run `kind load docker-image` or check `imagePullPolicy: IfNotPresent` in `deployment.yaml` |
| Pod `CrashLoopBackOff` | Model files missing inside image | Confirm `RUN python -m src.train` succeeded during `podman build` (check build logs) |
| `/health` returns `degraded` | Model artifacts not found at runtime | Check `kubectl logs <pod>` for path errors |

---

## Step 8 — (Optional) Deploy to GKE for Production

```bash
# 8a. Tag and push to a registry GKE can pull from
docker tag churn-api:latest gcr.io/<your-project>/churn-api:latest
docker push gcr.io/<your-project>/churn-api:latest

# 8b. Update the image field in kubernetes/deployment.yaml
#     image: gcr.io/<your-project>/churn-api:latest

# 8c. Apply to your GKE cluster (ensure kubectl context points to GKE)
kubectl config current-context
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
```

**Optional: serve via KServe instead of the raw Deployment**
```bash
kubectl apply -f kubernetes/kserve.yaml
```

---

## Day-2 Operations

### Retraining with new data
1. Replace or append to `data/raw/customer_churn.csv`.
2. Re-run `python -m src.train`.
3. Compare the new run against the previous one in the MLflow UI before promoting.
4. Rebuild the container image and redeploy (Steps 6–7).

### Rolling back a deployment
```bash
kubectl rollout undo deployment/churn-api
kubectl rollout status deployment/churn-api
```

### Checking current model metrics in production
```bash
curl http://<service-url>/metrics
```

### Common file locations
| What | Where |
|---|---|
| Trained model | `model/customer_churn.pkl` |
| Scaler | `model/scaler.pkl` |
| Feature column order | `model/feature_columns.pkl` |
| Latest metrics | `artifacts/metrics.json` |
| Confusion matrix | `artifacts/confusion_matrix.png` |
| Feature importance | `artifacts/feature_importance.csv` |
| MLflow tracking DB | `mlruns/mlflow.db` |

---

## CI Pipeline (`.github/workflows/ci.yml`)

Runs automatically on every push/PR to `main`:
```
checkout → install deps → train model → run pytest → lint (non-blocking) → build image
```
If CI fails at the "train model" step, reproduce locally with `python -m src.train` before debugging further.
