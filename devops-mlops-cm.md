### explain MLOps tools is to compare them with familiar DevOps tools. 

| MLOps Tool               | Similar DevOps Tool                         | Purpose                                        | Simple Demo Idea                            |
| ------------------------ | ------------------------------------------- | ---------------------------------------------- | ------------------------------------------- |
| **KServe**               | Helm + Kubernetes Deployment                | Deploy ML models as APIs with autoscaling      | Deploy a trained model using one YAML file  |
| **MLflow**               | Jenkins Build History + Artifact Repository | Track experiments, metrics, parameters, models | Train 3 models and compare accuracy         |
| **Kubeflow Pipelines**   | GitHub Actions / Jenkins Pipeline           | Automate ML workflow                           | Data → Training → Validation → Deploy       |
| **DVC**                  | Git for Large Files                         | Version datasets and ML models                 | Track CSV versions stored in S3             |
| **MinIO / S3**           | Artifact Storage                            | Store datasets, trained models, checkpoints    | Upload model.pkl and dataset.csv            |
| **Docker**               | Docker                                      | Package ML application                         | Containerize inference code                 |
| **Kubernetes**           | Kubernetes                                  | Run ML workloads                               | Run training/inference containers           |
| **Prometheus + Grafana** | Same                                        | Monitor models                                 | Monitor inference latency and request count |
| **ArgoCD**               | ArgoCD                                      | GitOps deployment                              | Automatically deploy updated model          |
| **Feast**                | Configuration Database                      | Feature Store                                  | Reuse features across models                |

---

### Think of an ML Project like this

```
Raw Data (CSV)
      │
      ▼
 DVC (Versions Dataset)
      │
      ▼
S3 / MinIO
      │
      ▼
Training
      │
      ▼
MLflow
(Experiments + Models)
      │
      ▼
Kubeflow Pipeline
(Automation)
      │
      ▼
KServe
(Model Serving)
      │
      ▼
Application
```

---

# KServe = Helm for Models

In DevOps

```
Helm install nginx
```

creates

* Deployment
* Service
* Ingress
* Autoscaling

Similarly,

```
kubectl apply -f sklearn.yaml
```

with KServe creates

* Model Server
* Service
* Autoscaling
* REST API
* Canary rollout (optional)

Instead of deploying an application, you're deploying a machine learning model.

---

# MLflow = Jenkins Build History

Imagine Jenkins.

Every build stores

* Build Number
* Logs
* Artifacts

MLflow stores

* Parameters

```
learning_rate=0.01
epochs=50
batch_size=32
```

* Metrics

```
Accuracy
Precision
Recall
Loss
```

* Model

```
model.pkl
```

* Code version

So MLflow is an experiment tracker for data scientists.

---

# Kubeflow Pipelines = CI/CD Pipeline

Instead of

```
Build
↓

Test
↓

Deploy
```

Kubeflow Pipeline is

```
Load Data
↓

Preprocess
↓

Train
↓

Evaluate
↓

Register Model
↓

Deploy
```

Every step runs automatically.

---

# DVC = Git for Data

Git works well for

```
main.py
app.py
Dockerfile
README.md
```

But not for

```
10 GB CSV

20 GB Images

Video Dataset
```

Git becomes slow.

DVC stores only metadata in Git.

Actual files go to

* S3
* MinIO
* Azure Blob
* GCS

Example

```
Git

train.py
predict.py
data.dvc
```

S3

```
customer.csv

images.zip

transactions.csv
```

DVC tracks which version of the dataset belongs to each model.

---

# Example

Dataset Version 1

```
customers.csv

1000 rows
```

Train

Accuracy

```
91%
```

Later

Dataset Version 2

```
customers.csv

5000 rows
```

Train again

Accuracy

```
96%
```

DVC allows you to restore the older dataset if needed.

```
dvc checkout
```

returns the previous dataset version.

---

# S3 / MinIO

Think of it as a central storage location.

Stores

```
datasets/

models/

checkpoints/

predictions/

logs/
```

Example

```
s3://ml-data/

customer.csv

house.csv

model.pkl

resnet50.pt
```

---

# SageMaker (AWS)

SageMaker combines many MLOps capabilities into a managed AWS service.

```
Notebook
      │
Training
      │
Experiment Tracking
      │
Model Registry
      │
Pipeline
      │
Deployment
      │
Monitoring
```

With open-source tools, you assemble the same workflow yourself.

```
Notebook → Jupyter

Tracking → MLflow

Pipeline → Kubeflow

Storage → S3 / MinIO

Serving → KServe

Monitoring → Prometheus

GitOps → ArgoCD
```

---

# Complete Open-Source MLOps Stack

```
Developer
     │
     ▼
GitHub
     │
     ▼
Kubeflow Pipeline
     │
     ├── Read Dataset
     │         │
     │         ▼
     │      DVC
     │         │
     │         ▼
     │     S3 / MinIO
     │
     ├── Train Model
     │
     ├── MLflow
     │     ├── Parameters
     │     ├── Metrics
     │     └── Model
     │
     ▼
KServe
     │
REST API
     │
Application
     │
Prometheus
     │
Grafana
```

## One-line analogy for presentations

* **Git** → Version control for source code.
* **DVC** → Version control for datasets and large model files (stored in S3/MinIO/GCS).
* **MLflow** → Tracks ML experiments, metrics, parameters, and model artifacts.
* **Kubeflow Pipelines** → CI/CD pipeline for ML workflows.
* **KServe** → Kubernetes-native model serving, similar to deploying an application with Helm.
* **S3/MinIO** → Object storage for datasets, models, and artifacts.
* **Model Registry (MLflow/SageMaker)** → Repository of approved model versions, similar to an artifact repository.
* **Prometheus + Grafana** → Monitor model APIs, latency, throughput, and errors.
* **SageMaker** → AWS managed platform that bundles training, experiment tracking, pipelines, model registry, deployment, and monitoring into a single service.
