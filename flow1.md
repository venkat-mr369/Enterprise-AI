I think this is the **best choice** for your Enterprise MLOps course. It is realistic, widely used in industry, and lets you teach every stage of the MLOps lifecycle without relying on a toy dataset.

# Enterprise MLOps Project

## Project Title

**E-Commerce Customer Churn Prediction Platform**

**Duration:** Entire 45-Day Course

## Business Problem

An e-commerce company wants to identify customers who are likely to stop shopping. If the company can predict churn early, it can offer discounts, loyalty rewards, or personalized campaigns to retain customers.

## Project Workflow

```text
Customer Data
      │
      ▼
Data Validation
      │
      ▼
Feature Engineering
      │
      ▼
Model Training
      │
      ▼
MLflow Experiment Tracking
      │
      ▼
Model Registry
      │
      ▼
Docker
      │
      ▼
GitHub
      │
      ▼
GitHub Actions
      │
      ▼
Cloud Build
      │
      ▼
Artifact Registry
      │
      ▼
GKE Deployment
      │
      ▼
Prediction API (FastAPI)
      │
      ▼
Prometheus
      │
      ▼
Grafana Dashboard
```

This also matches the CI/CD flow you've been using:
**GitHub → GitHub Actions → Cloud Build → Artifact Registry → GKE**.

---

# Dataset

Example customer records:

| CustomerID | Age | Gender | Orders | TotalSpend | LastOrderDays | LoginFrequency | SupportTickets | Membership | PaymentType | Churn |
| ---------- | --- | ------ | ------ | ---------- | ------------- | -------------- | -------------- | ---------- | ----------- | ----- |
| 1001       | 29  | Male   | 42     | 85000      | 5             | 18             | 0              | Gold       | UPI         | No    |
| 1002       | 45  | Female | 6      | 4200       | 95            | 2              | 5              | Silver     | Card        | Yes   |
| 1003       | 36  | Male   | 18     | 28000      | 30            | 8              | 1              | Gold       | Net Banking | No    |

---

# Folder Structure

```text
enterprise-mlops-churn/
│
├── data/
│
├── notebooks/
│
├── src/
│   ├── data_ingestion.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
│
├── api/
│   └── app.py
│
├── model/
│
├── mlruns/
│
├── Dockerfile
│
├── requirements.txt
│
├── deployment.yaml
│
├── service.yaml
│
├── github-actions.yml
│
└── README.md
```

---

# Technologies

### Programming

* Python

### ML

* Scikit-learn
* XGBoost

### API

* FastAPI

### Tracking

* MLflow

### Containerization

* Docker

### CI/CD

* GitHub
* GitHub Actions
* Cloud Build

### Registry

* Artifact Registry

### Kubernetes

* GKE

### Monitoring

* Prometheus
* Grafana

---

# Course Flow

### Week 1

* Understand the business problem
* Explore the dataset
* Data cleaning
* Feature engineering

Deliverable:

* Clean dataset

---

### Week 2

* Train multiple models
* Compare algorithms
* Evaluate performance
* Register the best model in MLflow

Deliverable:

* Best-performing model

---

### Week 3

* Build a FastAPI prediction service
* Package with Docker
* Test locally

Deliverable:

* Prediction API

---

### Week 4

* Push code to GitHub
* Configure GitHub Actions
* Trigger Cloud Build
* Store image in Artifact Registry
* Deploy to GKE

Deliverable:

* Live service running on Kubernetes

---

### Week 5

* Add Prometheus metrics
* Build Grafana dashboards
* Monitor API performance
* Monitor model latency
* Monitor request count

Deliverable:

* Production monitoring

---

### Week 6

* Add model versioning
* Implement rollback strategy
* Retrain with new data
* Redeploy updated model

Deliverable:

* Complete MLOps lifecycle

---

# Skills Students Will Learn

* Data preprocessing
* Feature engineering
* Machine learning model development
* Model evaluation
* MLflow experiment tracking
* Model registry
* FastAPI
* Docker
* Kubernetes
* GitHub Actions
* Cloud Build
* Artifact Registry
* GKE deployment
* Prometheus
* Grafana
* CI/CD automation
* Production monitoring
* Model versioning
* Model redeployment

This project closely resembles what many enterprises build for customer retention and provides an end-to-end production MLOps experience rather than a simple academic example. It is an excellent flagship project for your 45-day Enterprise MLOps course.
