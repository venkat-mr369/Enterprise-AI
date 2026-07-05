# Enterprise MLOps Engineering — Curriculum Mapped to Project Files

This adopts your reworked structure (Module → Section → Topics → Hands-on Lab)
and maps every Hands-on Lab to the actual file(s) already in
`enterprise-mlops-churn.zip`, including the `database/` module added for
Module 3. Order and module numbers below match your rework exactly — nothing
renumbered further.

Legend: ✅ Fully built · 🟡 Partially built (extend what exists) · ⬜ Net-new (not yet in zip)

---

# Module 1: Enterprise MLOps Fundamentals
**Status:** ✅ (all labs are environment setup, not code)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| 1. Intro to AI | Install VS Code, Python, Git; create GitHub repo/folder | The zip itself — first commit |
| 2. ML Fundamentals | Explore Customer Churn dataset | `data/raw/customer_churn.csv`, `notebooks/01_data_analysis.ipynb` |
| 3. Enterprise ML Lifecycle | Understand end-to-end workflow | `README.md` (architecture diagram), `RUNBOOK.md` |
| 4. Intro to MLOps | Review project architecture | `README.md` project structure section |

**Teach:** This module is pure orientation — hand students the zip on Day 1 and walk the tree top-down as a preview of Modules 2–16.

---

# Module 2: Python Essentials for MLOps
**Status:** ✅

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| 1. Python Basics | Read CSV, print customer records | `notebooks/01_data_analysis.ipynb` |
| 2. Working with Files | Read customer dataset (CSV/JSON, exceptions) | `src/data_ingestion.py` (`DataValidationError`, schema checks) |
| 3. Python Libraries | EDA with NumPy/Pandas/Matplotlib/sklearn | `notebooks/01_data_analysis.ipynb` against `data/raw/customer_churn.csv` |

**Teach:** Have students reproduce two or three notebook cells as standalone `.py` functions — a soft bridge into Module 3's real modules.

---

# Module 3: Database & Data Engineering
**Status:** ✅ core pipeline, ✅ database lab (built this week)

This is the module that changed most from your rework — "Database Design" is
now a first-class Section 1, not a side lab. The `database/` folder built
earlier fulfills it directly.

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| 1. Database Design | Create PostgreSQL database, execute `schema.sql` | `database/schema.sql` — creates `ml_ops_db`, role `ml_user`, schema `churn`, table `churn.customers` with constraints + indexes |
| 2. Data Ingestion | Build `data_ingestion.py` | `src/data_ingestion.py` (currently reads CSV — see extension note below) |
| 3. Data Cleaning | Build `preprocessing.py` | `src/preprocessing.py::clean_data`, `encode_categoricals` |
| 4. Feature Engineering | Build `feature_engineering.py` | `src/feature_engineering.py` (CLV, AvgMonthlySpend, TenureYears) |

**Extension included:** `database/generate_seed_data.py` + `database/load_data.py` seed 1,000 Indian-name records into `churn.customers` — gives Section 1's lab real data to query before Section 2 even starts.

**Teach — the natural lab sequence for this module:**
```
database/schema.sql            → create the database + table (Section 1)
        ↓
database/generate_seed_data.py → generate 1,000 records
        ↓
database/load_data.py          → load into churn.customers
        ↓
src/data_ingestion.py          → currently reads data/raw/customer_churn.csv
        ↓ (Section 2 lab extension)
        swap load_raw_data() for a SELECT * FROM churn.customers query
        (exact code for this swap is in database/README.md, bottom section)
        ↓
src/preprocessing.py → src/feature_engineering.py   (Sections 3–4, unchanged)
```

**One design decision for you:** right now `src/data_ingestion.py` reads the CSV and `database/` is a parallel, not-yet-connected lab. If you want Section 2's Hands-on Lab to be "connect the pipeline to Postgres" rather than "build a CSV reader," I'd add a config flag (`config.yaml: data_source: csv | postgres`) so `data_ingestion.py` can do either — that turns this into a proper lab exercise instead of a fait accompli. Say the word and I'll wire it in.

---

# Module 4: Machine Learning
**Status:** ✅

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| 1. Algorithms | Train multiple models | `src/train.py::build_models` (RandomForest, XGBoost), `config/model_config.yaml` |
| 2. Evaluation | Build `train.py` / `evaluate.py` | `src/train.py`, `src/evaluate.py` (Accuracy/Precision/Recall/F1/ROC-AUC + confusion matrix + feature importance) |

**Teach:** Run `python -m src.train` once end-to-end, then have students edit `config/model_config.yaml` hyperparameters and re-run to see metrics move — reinforces config-driven training.

---

# Module 5: FastAPI
**Status:** ✅ (Uvicorn covered; Gunicorn not yet added)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| REST APIs, FastAPI, Swagger, Request Validation, Error Handling, Uvicorn | Build `predict.py`, `api/app.py` | `src/predict.py` (`ChurnPredictor`), `api/app.py` (`/`, `/health`, `/predict`, `/metrics`; Pydantic validation; Swagger auto-served at `/docs`) |

**To add for full topic coverage:** Gunicorn + Uvicorn worker pattern for production:
```bash
gunicorn api.app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Teach:** This now lands right after Module 4 in your rework, which is the right call — students get a working, testable API before touching any infra tooling. `tests/test_api.py` gives them an immediate way to verify it.

---

# Module 6: Containerization with Podman & Docker
**Status:** ✅

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| Docker Architecture, Podman vs Docker, Images, Dockerfile, Containerfile, Docker Compose | Build image, run locally with Podman | `Dockerfile`, `Containerfile` (identical, per your Podman-first workflow), `docker-compose.yml` (API + MLflow UI services) |

**To add:** multi-stage build as an image-size/security optimization exercise — split the current single-stage `Dockerfile` into a `builder` stage (pip install) and a slim `runtime` stage.

---

# Module 7: Kubernetes
**Status:** ✅ Deployments/Services/Ingress; ⬜ ConfigMaps/Secrets/Autoscaling not yet added

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| Pods, Deployments, Services, Ingress | Create `deployment.yaml`, `service.yaml`, `ingress.yaml` | `kubernetes/deployment.yaml` (probes + resource limits already set), `kubernetes/service.yaml`, `kubernetes/ingress.yaml` |
| ConfigMaps, Secrets, Autoscaling | *(net-new)* | Not yet in zip — natural lab: turn `config/config.yaml` into a `ConfigMap`, add an `HPA` manifest |

**Teach:** Students already have a tested runbook for this (see `RUNBOOK.md` Step 7 — Kind/Minikube). This module's lab is deploying what they already have, then extending it with ConfigMaps/Secrets/HPA as new manifests.

---

# Module 8: Data Version Control (DVC)
**Status:** 🟡 (placeholder only — real S3 remote not wired up)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| DVC, Pipelines, AWS S3 Remote, Dataset/Model Versioning | Configure DVC, upload to AWS S3 | `.dvc/config` (placeholder) |

**Lab to build:**
```bash
dvc init
dvc add data/raw/customer_churn.csv
dvc remote add -d storage s3://<bucket>/dvc-store
dvc push
```
Now that Module 3 has a real database, a good extended lab is versioning a `database/seed_customers.csv` **export** rather than the static raw CSV — closer to how enterprise teams snapshot a live table for reproducible training.

---

# Module 9: MLflow
**Status:** 🟡 (Tracking works via SQLite; PostgreSQL backend + Model Registry not yet added)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| Tracking, Experiments, Metrics, Artifacts | Configure MLflow, compare experiments | `src/train.py` (MLflow logging calls), `config/config.yaml::mlflow` — currently `sqlite:///mlruns/mlflow.db` |
| Model Registry, PostgreSQL Backend Store | *(net-new)* | Swap `tracking_uri` to a Postgres connection string — you already have a Postgres instance from Module 3's `database/` setup, so this is a natural reuse rather than standing up new infra |

**Teach — nice continuity moment:** point out that the same RDS/Postgres instance from Module 3 (`ml_ops_db`) can host the MLflow backend store too, just in a separate schema (e.g. `mlflow`) — reinforces "one database, multiple enterprise uses" rather than treating Postgres as a one-off Module 3 artifact.

---

# Module 10: Kubernetes Model Serving with KServe
**Status:** 🟡 (manifest exists; not yet deployed against a live cluster)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| KServe, InferenceService, Serverless Inference, Canary, Auto Scaling | Deploy model with KServe | `kubernetes/kserve.yaml` |

**Teach:** Compare directly against Module 7's plain `Deployment` — same image, different serving abstraction. Good moment to discuss when KServe's extra machinery (canary, multi-model) is worth the complexity.

---

# Module 11: Kubeflow
**Status:** ⬜ Not yet built

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| Kubeflow Pipelines, Katib, Notebook Servers | Create Kubeflow Pipeline | *(net-new)* |

**Teach:** The existing `src/` functions (`data_ingestion` → `preprocessing` → `feature_engineering` → `train` → `evaluate`) are already single-purpose and composable — that's exactly the shape Kubeflow Pipeline components need, so this module is mostly wrapping, not rewriting.

---

# Module 12: AWS MLOps
**Status:** ⬜ Not yet built (Postgres/RDS from Module 3 gives a head start on IAM/networking concepts)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| IAM, S3, EC2, ECR, CloudWatch, SageMaker | Train and deploy on SageMaker | *(net-new)* — reuse `src/train.py` logic inside a SageMaker training job/script-mode entry point |

**Teach:** Frame as "same ML logic, different execution environment" — the `src/` modules don't change, only what orchestrates them does.

---

# Module 13: CI/CD & GitOps
**Status:** 🟡 (GitHub Actions covered; Cloud Build/Artifact Registry/Argo CD not yet added)

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| GitHub Actions | Build CI/CD pipeline | `.github/workflows/ci.yml` (train → test → build image) |
| Cloud Build, Artifact Registry, Argo CD, GitOps | *(net-new)* | Extend `ci.yml` with a push-to-registry step; add `cloudbuild.yaml` + an Argo CD `Application` manifest watching `kubernetes/` |

---

# Module 14: Monitoring & Observability
**Status:** ⬜ Not yet built

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| Prometheus, Grafana, Logging, API Metrics, Model/Data Drift | Build monitoring dashboards | *(net-new)* |

**Naming collision to flag for the lab:** `api/app.py` already has a `/metrics` endpoint, but it returns **model evaluation** metrics (accuracy, ROC-AUC) from `artifacts/metrics.json` — not Prometheus-style operational metrics (request count, latency). Decide as a class exercise: split into `/metrics` (Prometheus) and `/model-metrics` (current behavior), or keep one endpoint serving both shapes.

---

# Module 15: Enterprise Security
**Status:** ⬜ Not yet built

| Section | Hands-on Lab | Project File(s) |
|---|---|---|
| IAM, RBAC, Secrets Management | Secure Kubernetes deployment | *(net-new)* — `ServiceAccount`/`Role`/`RoleBinding` manifests for `kubernetes/`; convert `config/config.yaml` secrets into a K8s `Secret` |

**Good tie-back:** the `ml_user` least-privilege pattern from Module 3's `database/schema.sql` is the same principle this module teaches at the Kubernetes/IAM layer — worth calling out explicitly as a recurring enterprise theme, not a one-off DB detail.

---

# Module 16: Enterprise Capstone Project
**Status:** ✅ core / 🟡 full enterprise flow

Not a new build — students assemble everything from Modules 1–15 into one
deployed system.

**Already working end-to-end today (✅):**
```
database/schema.sql → seed data → src/data_ingestion.py (CSV path)
→ src/preprocessing.py → src/feature_engineering.py → src/train.py
→ MLflow (SQLite) → api/app.py (FastAPI) → Dockerfile/Containerfile
→ GitHub Actions (CI) → kubernetes/deployment.yaml,service.yaml,ingress.yaml
```

**What Modules 8–10, 13 extend (🟡):**
```
+ DVC/S3 · + MLflow PostgreSQL backend + Registry · + KServe · + Cloud Build/Artifact Registry/Argo CD
```

**What Modules 11, 12, 14, 15 add net-new (⬜):**
```
+ Kubeflow Pipelines/Katib · + AWS SageMaker path · + Prometheus/Grafana/Drift · + RBAC/Secrets
```

**Final deliverables checklist (from your rework):**
- [x] GitHub Repository
- [x] FastAPI Prediction Service
- [x] Docker & Podman Image
- [x] Kubernetes Deployment
- [x] Database (PostgreSQL, Module 3)
- [ ] DVC Integration
- [ ] MLflow Registry (Postgres-backed)
- [ ] KServe Deployment (built, not yet cluster-tested)
- [ ] Kubeflow Pipeline
- [ ] AWS SageMaker Deployment
- [ ] CI/CD Pipeline (GitHub Actions done, Cloud Build/Argo CD pending)
- [ ] Prometheus & Grafana Dashboard

---

## Suggested Build Order for Instructors (matches your rework)

1. **Modules 1–2:** teach directly from the zip, no changes needed.
2. **Module 3:** teach `database/` (Section 1) → `src/data_ingestion.py` (Section 2, optionally extended to query Postgres) → `src/preprocessing.py` → `src/feature_engineering.py`.
3. **Modules 4–7:** teach directly from the zip as-is.
4. **Modules 8–9:** extension labs on existing `.dvc/config` and MLflow SQLite setup.
5. **Module 10:** extension lab on existing `kserve.yaml`.
6. **Modules 11–12:** net-new builds, output plugs back into the same repo.
7. **Module 13:** extension lab on existing `ci.yml`.
8. **Modules 14–15:** net-new builds.
9. **Module 16:** integration only — no new code, assemble everything above.

---

## Open Question for You

Section 2 of Module 3 ("Data Ingestion") currently has two independent paths in
the zip — CSV (`src/data_ingestion.py`) and Postgres (`database/`) — that
don't talk to each other yet. Want me to wire `data_ingestion.py` to read from
`churn.customers` (with a config flag to fall back to CSV), so Module 3's lab
is "connect the two," rather than two separate exercises?