# Enterprise MLOps Engineering Course — Module-to-Project Mapping

This maps the 16-module, 45-day curriculum to the files already in
`enterprise-mlops-churn.zip`, so each module's lab points students at a
real, working piece of the capstone rather than an abstract exercise.

Legend: ✅ Covered by current zip · 🟡 Partially covered (structure exists, needs extension) · ⬜ Not yet built (to add in a later pass)

---

## Module 1 — Introduction to Enterprise MLOps
**Status:** ✅

| Use | File(s) |
|---|---|
| Show the whole enterprise architecture end-to-end | `README.md` (flow diagram), `RUNBOOK.md` |
| "Set up Python dev environment" lab | `requirements.txt`, Step 1 of `RUNBOOK.md` |
| "Create GitHub repository" lab | `.gitignore`, `LICENSE`, `.github/workflows/ci.yml` (push this repo as the first commit) |

**Teach:** Walk through the folder tree top to bottom as the "map" of the whole 45-day course — every later module fills in one branch of it.

---

## Module 2 — Python Essentials for MLOps
**Status:** ✅

| Use | File(s) |
|---|---|
| Variables, loops, functions, modules | `src/utils.py`, `src/config.py` — small, readable, real examples |
| Working with CSV / Pandas / NumPy | `notebooks/01_data_analysis.ipynb` |
| Exception handling pattern | `src/data_ingestion.py` → `DataValidationError` |
| "Customer Dataset Exploration" lab | `notebooks/01_data_analysis.ipynb` against `data/raw/customer_churn.csv` |

**Teach:** Have students run each cell of `01_data_analysis.ipynb`, then re-implement one cell as a plain `.py` script to bridge notebook → module thinking.

---

## Module 3 — Data Engineering & Feature Engineering
**Status:** ✅

| Use | File(s) |
|---|---|
| Data validation | `src/data_ingestion.py` (`validate_schema`, `REQUIRED_COLUMNS`) |
| Missing values / duplicates | `src/preprocessing.py::clean_data` |
| Encoding | `src/preprocessing.py::encode_categoricals` |
| Feature engineering (CLV, avg spend) | `src/feature_engineering.py` |
| Train/test split | `src/train.py::split_features_target` + `train_test_split` call |
| "Customer Churn Dataset Preparation" lab | `notebooks/02_feature_engineering.ipynb` |

**Teach:** This module is effectively `src/data_ingestion.py` → `src/preprocessing.py` → `src/feature_engineering.py`, in that order. Have students add one new engineered feature (e.g., `AvgTicketSize`) as the lab deliverable.

---

## Module 4 — Machine Learning for Enterprise
**Status:** ✅

| Use | File(s) |
|---|---|
| Classification, Random Forest, XGBoost | `src/train.py::build_models`, `config/model_config.yaml` |
| Model evaluation (Accuracy/Precision/Recall/F1/ROC-AUC) | `src/evaluate.py::evaluate_model` |
| Hyperparameter tuning | `config/model_config.yaml` (have students hand-tune, then later automate with Katib in Module 12) |
| "Build Customer Churn Prediction Model" lab | `python -m src.train` end to end |

**Teach:** Run `src/train.py` once, then have students change `n_estimators` / `max_depth` in `config/model_config.yaml` and re-run to see metrics shift — reinforces that config-driven training is the enterprise pattern (no hardcoded hyperparameters).

---

## Module 5 — Git & Data Version Control (DVC)
**Status:** 🟡 (Git fully covered; DVC is a placeholder — S3 remote not wired up)

| Use | File(s) |
|---|---|
| Git fundamentals / GitHub workflow | The zip itself, once pushed to a repo |
| DVC config placeholder | `.dvc/config` |
| **To add:** `dvc init`, `dvc add data/raw/customer_churn.csv`, configure S3 remote | Not yet in zip — Module 5 lab |

**Teach:** This is the first "extend the scaffold yourself" module. Have students run:
```bash
dvc init
dvc add data/raw/customer_churn.csv
dvc remote add -d storage s3://<bucket>/dvc-store
dvc push
```
and commit the resulting `.dvc` file alongside the code.

---

## Module 6 — Experiment Tracking with MLflow
**Status:** 🟡 (Tracking fully covered; Model Registry + PostgreSQL backend not yet wired)

| Use | File(s) |
|---|---|
| Experiments, runs, params, metrics, artifacts | `src/train.py` (MLflow calls), `config/config.yaml::mlflow` |
| MLflow UI | `mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db` |
| **To add:** PostgreSQL backend, Model Registry, model promotion (staging → production) | Currently uses SQLite — swap `tracking_uri` to a Postgres connection string as the Module 6 lab |

**Teach:** Students already have working tracking from Module 4's lab. This module upgrades the backend (SQLite → PostgreSQL) and adds `mlflow.register_model(...)` calls in `src/train.py` for the registry + promotion workflow.

---

## Module 7 — Enterprise Model Deployment & Serving
**Status:** ✅

| Use | File(s) |
|---|---|
| FastAPI, Swagger, Uvicorn | `api/app.py` (Swagger auto-available at `/docs`) |
| Input validation | `api/app.py::CustomerRecord` (Pydantic model) |
| Error handling | `api/app.py` (`HTTPException` on missing model / bad input) |
| **To add:** Gunicorn for production WSGI, basic load testing | Not yet in zip — Module 7 lab extension |
| "Build Customer Churn Prediction API" lab | `api/app.py` + `tests/test_api.py` |

**Teach:** Run the API with `--reload` first (dev mode), then have students run it under Gunicorn + Uvicorn workers for the production-pattern comparison:
```bash
gunicorn api.app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

---

## Module 8 — Docker for Enterprise MLOps
**Status:** ✅ (basic image works; multi-stage build not yet added)

| Use | File(s) |
|---|---|
| Dockerfile | `Dockerfile` / `Containerfile` |
| Docker Compose | `docker-compose.yml` (API + MLflow UI services) |
| **To add:** multi-stage build to shrink image size | Module 8 lab: split into a `builder` stage (pip install) and a slim `runtime` stage |
| "Build Docker Image / Push to Registry" lab | `podman build` / `docker build`, then push to Artifact Registry or ECR |

**Teach:** Current `Dockerfile` is single-stage for clarity in earlier modules. This is the module where students refactor it into multi-stage as a size/security optimization exercise — a good "before/after image size" demo.

---

## Module 9 — Kubernetes for MLOps
**Status:** ✅ (Deployment/Service/Ingress covered; ConfigMaps, Secrets, HPA, PVs not yet added)

| Use | File(s) |
|---|---|
| Pods, Deployments | `kubernetes/deployment.yaml` |
| Services | `kubernetes/service.yaml` |
| Ingress Controller | `kubernetes/ingress.yaml` |
| Resource limits, liveness/readiness probes | Already set in `kubernetes/deployment.yaml` |
| **To add:** ConfigMap for `config/config.yaml`, Secret for any credentials, HPA, rolling update strategy | Module 9 lab extensions |
| "Deploy API on Kubernetes" lab | Step 7 of `RUNBOOK.md` |

**Teach:** Students already deployed the raw manifests in the RUNBOOK. This module's lab converts `config/config.yaml` into a `ConfigMap` mounted into the pod, and adds a `HorizontalPodAutoscaler` manifest.

---

## Module 10 — Enterprise Model Serving with KServe
**Status:** 🟡 (manifest exists; not yet deployed/tested against a live cluster)

| Use | File(s) |
|---|---|
| InferenceService | `kubernetes/kserve.yaml` |
| **To add:** Canary/Blue-Green deployment config, autoscaling annotations | Module 10 lab extension on top of `kserve.yaml` |
| "Deploy Model with KServe" lab | `kubectl apply -f kubernetes/kserve.yaml` (requires KServe installed on the cluster) |

**Teach:** Compare this against Module 9's plain `Deployment` — same container image, different serving abstraction. Good moment to discuss when KServe's extra features (canary, multi-model) earn their complexity.

---

## Module 11 — CI/CD & GitOps for MLOps
**Status:** 🟡 (GitHub Actions covered; Cloud Build → Artifact Registry → Argo CD not yet added)

| Use | File(s) |
|---|---|
| GitHub Actions | `.github/workflows/ci.yml` (train → test → build image) |
| **To add:** Cloud Build config, Artifact Registry push step, Argo CD Application manifest | Module 11 lab — extend `ci.yml` and add `cloudbuild.yaml` + `argocd-app.yaml` |
| Lab flow: GitHub → GitHub Actions → Cloud Build → Artifact Registry → Argo CD → GKE | Builds directly on `ci.yml`'s existing `build-image` job |

**Teach:** `ci.yml` already stops at "build the image." This module's lab adds the push-to-registry step and a GitOps sync via Argo CD watching the `kubernetes/` folder.

---

## Module 12 — Kubeflow
**Status:** ⬜ Not yet built

| Use | File(s) |
|---|---|
| Kubeflow Pipelines equivalent of `src/train.py` | To be added: a Kubeflow pipeline that wraps `data_ingestion → preprocessing → feature_engineering → train → evaluate` as pipeline components |
| Katib for hyperparameter tuning | Replaces the manual `config/model_config.yaml` tuning from Module 4 |

**Teach:** This is the first fully new module. The existing `src/` functions are already broken into clean, single-purpose steps — that's exactly what Kubeflow Pipeline components need, so converting them is mostly wrapping, not rewriting.

---

## Module 13 — AWS MLOps
**Status:** ⬜ Not yet built

| Use | File(s) |
|---|---|
| S3 for data | Extends the Module 5 DVC remote |
| ECR for the image | Alternative registry target to Module 11's Artifact Registry |
| SageMaker training/registry/endpoints | New: a SageMaker equivalent of `src/train.py` + `model/` artifacts |

**Teach:** Frame this as "the same pipeline, different cloud" — reinforces that the ML logic in `src/` is cloud-agnostic; only the infra around it changes.

---

## Module 14 — Monitoring & Observability
**Status:** ⬜ Not yet built

| Use | File(s) |
|---|---|
| API monitoring | Instrument `api/app.py` with a `/metrics` Prometheus exporter (distinct from the existing `/metrics` model-metrics endpoint — will need a naming decision) |
| Data/concept/model drift | New module comparing incoming request distributions to `data/raw/customer_churn.csv` |
| Dashboards | Grafana dashboard JSON, to be added |

**Teach:** Note the naming collision up front: the existing `/metrics` in `api/app.py` returns *model evaluation* metrics (accuracy, ROC-AUC), while Prometheus conventionally scrapes `/metrics` for *operational* metrics (request count, latency). Good lab discussion: should these be the same endpoint or split into `/metrics` and `/model-metrics`?

---

## Module 15 — Enterprise Security & Production Architecture
**Status:** ⬜ Not yet built (RBAC, Secrets, Network Policies)

| Use | File(s) |
|---|---|
| Secrets management | Convert any hardcoded config in `config/config.yaml` into a Kubernetes `Secret` |
| RBAC | New: `ServiceAccount` + `Role` + `RoleBinding` manifests for `kubernetes/` |
| Multi-environment (Dev/QA/UAT/Prod) | New: `kubernetes/overlays/{dev,qa,uat,prod}/` using Kustomize on top of the existing base manifests |

**Teach:** The existing `kubernetes/` folder becomes the Kustomize "base"; this module's lab is building environment-specific overlays on top of it.

---

## Module 16 — Enterprise Capstone Project
**Status:** ✅ core pipeline / 🟡 full enterprise flow

The full target architecture from the course:

```
Customer Data → Data Validation → Feature Engineering → DVC (AWS S3)
→ Model Training → MLflow Tracking → MLflow Model Registry (PostgreSQL)
→ Docker Image → GitHub → GitHub Actions → Cloud Build → Artifact Registry
→ Argo CD → GKE/AKS → Ingress Controller → KServe → FastAPI Inference API
→ Prometheus → Grafana → Model Monitoring → Data Drift Detection → Model Retraining
```

**What's already built (zip, ✅):**
```
Customer Data → Data Validation → Feature Engineering → Model Training
→ MLflow Tracking → Docker Image → GitHub Actions (CI) → GKE (Deployment/Service/Ingress)
→ FastAPI Inference API
```

**What Modules 5, 6, 10, 11 extend (🟡):**
```
+ DVC/S3 · + Model Registry/PostgreSQL · + KServe · + Cloud Build/Artifact Registry/Argo CD
```

**What Modules 12–15 add net-new (⬜):**
```
+ Kubeflow Pipelines/Katib · + AWS SageMaker path · + Prometheus/Grafana/Drift detection · + RBAC/Secrets/Multi-env
```

**Teach:** By Module 16, students aren't building a new project — they're assembling every prior module's lab output into the single end-to-end flow above. The capstone deliverable is a working GKE deployment with monitoring and CI/CD, built entirely from pieces they already have.

---

## Suggested Build Order for Instructors

Since the zip currently gives you Modules 1–4, 7–9 fully working, and 5/6/10/11 partially working, a practical teaching sequence is:

1. Teach 1–4 directly from the zip as-is (no changes needed).
2. Teach 5–6 as "extend what you have" labs (DVC remote, Postgres backend, Model Registry).
3. Teach 7–9 directly from the zip as-is.
4. Teach 10–11 as extension labs on the existing `kserve.yaml` and `ci.yml`.
5. Build 12–15 as net-new modules, each producing artifacts that plug into the same `enterprise-mlops-churn/` repo.
6. Module 16 is an integration exercise, not new code — assemble everything above into the one deployed system.
