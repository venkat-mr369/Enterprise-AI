# RUNBOOK — Enterprise Customer Churn Prediction Platform (with PostgreSQL)

Operational guide for taking this project from a fresh clone to a running
Kubernetes deployment, **including the PostgreSQL database module**
(`database/`) added in Module 3-A. Follow the steps in order the first
time; after that, jump to whichever section you need.

---

## Flow at a Glance

```
Extract / Clone
      ↓
venv + pip install
      ↓
PostgreSQL setup (schema.sql → seed data → load into ml_ops_db)
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
unzip enterprise-mlops-churn-pgdb.zip
cd enterprise-mlops-churn

# 1b. Create an isolated Python environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 1c. Install core dependencies
pip install -r requirements.txt

# 1d. Install the database module's extra dependencies
pip install -r database/requirements-db.txt
```

**Verify:**
```bash
python -c "import fastapi, sklearn, xgboost, mlflow, psycopg2, faker; print('ok')"
```
Expected output: `ok`

---

## Step 2 — Set Up PostgreSQL (Module 3-A)

This is the new step compared to the CSV-only version of this project.
It stands up a real PostgreSQL database, a least-privilege application
user, and seeds 1,000 Indian-name customer records — either on a local
Postgres instance or Amazon RDS.

> **Port note:** PostgreSQL's default port is `5432`, not `3306` (that's
> MySQL's default). All commands below assume `5432` — confirm the actual
> port on your RDS instance's console page if you're using RDS.

### 2a. Create the database, role, and schema

Run as the RDS **master user** (or local `postgres` superuser):

```bash
psql -h <endpoint> -p 5432 -U <master_user> -d postgres -f database/schema.sql
```

This creates:
- Database `ml_ops_db`
- Least-privilege role `ml_user` (application code never uses the master user)
- Schema `churn`, owned by `ml_user`
- Table `churn.customers`, matching the ML pipeline's feature set plus Indian-context columns (`city`, `state`, INR pricing)

**About the password:** `schema.sql` ships with a placeholder strong
password (`ChurnDB_2026_!Xk7pQ9vR`) as an example only. Generate your own
before using a real database:
```bash
openssl rand -base64 24
```
Then either edit `schema.sql` before running it, or afterward run:
```sql
ALTER ROLE ml_user WITH PASSWORD '<new-password>';
```

### 2b. Configure credentials

```bash
cp database/.env.example database/.env
# edit database/.env with your real DB_HOST / DB_PASSWORD
export $(grep -v '^#' database/.env | xargs)
```

Local Postgres: set `DB_HOST=127.0.0.1` and `DB_SSLMODE=prefer`.
Amazon RDS: keep `DB_SSLMODE=require`.

### 2c. Generate 1,000 Indian-name customer records

```bash
cd database
python generate_seed_data.py --count 1000 --out seed_customers.csv
cd ..
```

Uses `Faker("en_IN")` for realistic Indian names, paired with 12 Indian
states/cities and INR-scaled pricing (₹299–₹2,999/month). Churn
likelihood follows the same logic as the core dataset (month-to-month +
fiber + low tenure + high charges → higher churn).

### 2d. Load into PostgreSQL

```bash
cd database
python load_data.py --csv seed_customers.csv
cd ..
```

Expected output:
```
Inserted (or skipped existing) 1000 rows into churn.customers
Total rows in table: 1000
Churn breakdown: [('No', 391), ('Yes', 609)]
```

The load is idempotent — re-running it won't duplicate rows.

### 2e. Verify

```bash
psql -h <endpoint> -p 5432 -U ml_user -d ml_ops_db
```
```sql
SELECT count(*) FROM churn.customers;
SELECT churn, count(*) FROM churn.customers GROUP BY churn;
SELECT state, count(*) FROM churn.customers GROUP BY state ORDER BY 2 DESC;
```

**Troubleshooting**
| Symptom | Cause | Fix |
|---|---|---|
| `psql: error: connection refused` | Wrong host/port, or security group blocks your IP | Check RDS security group inbound rules; confirm port is `5432` |
| `FATAL: password authentication failed` | Wrong password, or ran the script as `ml_user` instead of master user for Step 2a | Re-run `schema.sql` as the master/superuser |
| `DB_PASSWORD is not set` when running `load_data.py` | `.env` not exported into the shell | Re-run `export $(grep -v '^#' database/.env \| xargs)` in the same terminal session |

---

## Step 3 — Run the Training Pipeline

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

> **Current status:** the training pipeline still reads from
> `data/raw/customer_churn.csv`, independently of the PostgreSQL table you
> just populated in Step 2. The two data sources are statistically
> consistent but not yet connected. See **Step 3a** below to bridge them.

### Step 3a (optional) — Point ingestion at PostgreSQL instead of the CSV

To make `src/data_ingestion.py` read from `churn.customers` instead of the
CSV, swap `load_raw_data()` for a query like:

```python
import pandas as pd
import psycopg2
import os

def load_raw_data_from_db():
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"], port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "ml_ops_db"),
        user=os.environ.get("DB_USER", "ml_user"),
        password=os.environ["DB_PASSWORD"],
        sslmode=os.environ.get("DB_SSLMODE", "prefer"),
    )
    return pd.read_sql("SELECT * FROM churn.customers;", conn)
```

Note the column names differ slightly (`customer_id` vs `customerID`,
`tenure_months` vs `tenure`, INR-denominated charges) — you'll need to
rename columns to match `REQUIRED_COLUMNS` in `data_ingestion.py`, or
update that list to match the database schema. This is intentionally left
as a lab exercise rather than pre-wired, so students practice reconciling
two schemas — a common real-world data engineering task.

**Verify (either path):**
```bash
ls model/            # customer_churn.pkl, scaler.pkl, feature_columns.pkl
cat artifacts/metrics.json
```

---

## Step 4 — Inspect Results with MLflow

```bash
mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db
```
Open **http://localhost:5000** and compare the `random_forest` vs
`xgboost` runs — parameters, metrics, and logged model artifacts side by
side.

> **Enterprise upgrade path:** the same PostgreSQL instance from Step 2
> can host the MLflow backend store too, in a separate schema (e.g.
> `mlflow`), instead of SQLite. This is the natural Module 9 lab
> extension — one database, multiple enterprise uses.

---

## Step 5 — Run and Test the API Locally

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

---

## Step 6 — Run the Test Suite

```bash
pytest tests/ -v
```

Covers: data ingestion, preprocessing, feature engineering, prediction
correctness, and all API endpoints (11 tests total).

---

## Step 7 — Build and Run the Container (Podman)

```bash
podman build -t churn-api:latest -f Containerfile .
podman run -p 8000:8000 churn-api:latest
```

Docker works identically — swap `podman` → `docker` and `Containerfile` →
`Dockerfile`.

```bash
podman compose up      # or: docker compose up
```

> If you wired Step 3a (Postgres ingestion), the container will also need
> `DB_HOST`/`DB_PASSWORD`/etc. passed in as environment variables or a
> mounted `.env` — add an `env_file: database/.env` line to
> `docker-compose.yml`'s `churn-api` service.

**Verify:**
```bash
curl http://localhost:8000/health
```

---

## Step 8 — Deploy to Local Kubernetes (Kind or Minikube)

```bash
# 8a. Start a local cluster
kind create cluster --name churn-cluster     # or: minikube start

# 8b. Load the image into the cluster
kind load docker-image churn-api:latest --name churn-cluster

# 8c. Apply manifests
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

# 8d. Verify
kubectl get pods
kubectl port-forward svc/churn-api-service 8000:80
curl http://localhost:8000/health
```

**Troubleshooting**
| Symptom | Cause | Fix |
|---|---|---|
| Pod stuck in `ImagePullBackOff` | Image not loaded into cluster | Re-run `kind load docker-image` |
| Pod `CrashLoopBackOff` | Model files missing inside image | Confirm `RUN python -m src.train` succeeded during build |
| `/health` returns `degraded` | Model artifacts not found at runtime | Check `kubectl logs <pod>` |

---

## Step 9 — (Optional) Deploy to GKE for Production

```bash
# 9a. Tag and push to a registry GKE can pull from
docker tag churn-api:latest gcr.io/<your-project>/churn-api:latest
docker push gcr.io/<your-project>/churn-api:latest

# 9b. Update the image field in kubernetes/deployment.yaml

# 9c. Apply to your GKE cluster
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
1. Add new rows to `churn.customers` (via `load_data.py` or directly), or update `data/raw/customer_churn.csv`.
2. Re-run `python -m src.train`.
3. Compare the new run against the previous one in the MLflow UI before promoting.
4. Rebuild the container image and redeploy (Steps 7–8).

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
| Database schema/setup | `database/schema.sql` |
| Seed data generator | `database/generate_seed_data.py` |
| Database loader | `database/load_data.py` |
| DB credentials template | `database/.env.example` |
| Trained model | `model/customer_churn.pkl` |
| Scaler | `model/scaler.pkl` |
| Feature column order | `model/feature_columns.pkl` |
| Latest metrics | `artifacts/metrics.json` |
| MLflow tracking DB | `mlruns/mlflow.db` |

---

## CI Pipeline (`.github/workflows/ci.yml`)

Runs automatically on every push/PR to `main`:
```
checkout → install deps → train model → run pytest → lint (non-blocking) → build image
```
This currently trains against the CSV dataset, not PostgreSQL — if you
wire Step 3a into the main pipeline, add a PostgreSQL service container
to the CI workflow (or a hosted test database) so ingestion has something
to connect to during the `train` step.

If CI fails at the "train model" step, reproduce locally with
`python -m src.train` before debugging further.
