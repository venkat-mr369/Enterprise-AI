# Module 1: Enterprise MLOps Fundamentals

## Objective

 **Enterprise E-Commerce Customer Churn Prediction Platform**
Understand machine learning, MLOps, enterprise workflows, and the capstone project.

### Section 1: Introduction to Artificial Intelligence

#### Topics

* What is Artificial Intelligence (AI)?
* What is Machine Learning (ML)?
* What is Deep Learning (DL)?
* AI vs ML vs DL
* Real-world AI use cases
* E-commerce AI use cases

**Hands-on Lab**

* Install VS Code
* Install Python
* Install Git
* Create GitHub account
* Create GitHub repository
* Create project folder

---

### Section 2: Machine Learning Fundamentals

#### Topics

* What is a Machine Learning Model?
* Types of Machine Learning
* Classification
* Regression
* Clustering
* Supervised Learning
* Unsupervised Learning
* Reinforcement Learning

**Hands-on Lab**

* Explore the Customer Churn dataset
* Understand business requirements

---

### Section 3: Enterprise ML Lifecycle

#### Topics

* Business Problem
* Data Collection
* Data Validation
* Feature Engineering
* Model Training
* Evaluation
* Deployment
* Monitoring
* Retraining

**Hands-on Lab**

* Understand the end-to-end workflow of the project

---

### Section 4: Introduction to MLOps

#### Topics

* Traditional ML vs MLOps
* Why MLOps?
* Enterprise MLOps Architecture
* Data Scientist vs ML Engineer vs MLOps Engineer
* DevOps vs MLOps
* Team collaboration

**Hands-on Lab**

* Review project architecture

---

# Module 2: Python Essentials for MLOps

## Objective

Learn only the Python required to build the project.

### Section 1: Python Basics

#### Topics

* Variables
* Data Types
* Operators
* Functions
* Lists
* Tuples
* Dictionaries
* Loops
* Conditional Statements

**Hands-on Lab**

* Read CSV
* Print customer records

---

### Section 2: Working with Files

#### Topics

* CSV
* JSON
* File Handling
* Exception Handling

**Hands-on Lab**

* Read customer dataset

---

### Section 3: Python Libraries

#### Topics

* NumPy
* Pandas
* Matplotlib
* Scikit-learn Basics

**Hands-on Lab**

* Perform exploratory data analysis (EDA)

---

# Module 3: Database & Data Engineering

## Objective

Create and prepare the enterprise dataset.

### Section 1: Database Design

#### Topics

* PostgreSQL Installation
* Database Design
* Customer Schema
* Tables
* Constraints
* Indexes

**Hands-on Lab**

* Create PostgreSQL database
* Execute schema.sql

---

### Section 2: Data Ingestion

#### Topics

* CSV Files
* SQL Data
* Pandas DataFrames
* Data Validation

**Hands-on Lab**

* Build `data_ingestion.py`

---

### Section 3: Data Cleaning

#### Topics

* Missing Values
* Duplicate Records
* Invalid Data
* Outliers

**Hands-on Lab**

* Build `preprocessing.py`

---

### Section 4: Feature Engineering

#### Topics

* Label Encoding
* One-Hot Encoding
* Scaling
* Feature Selection
* Customer Lifetime Value
* Average Order Value
* Order Frequency

**Hands-on Lab**

* Build `feature_engineering.py`

---

# Module 4: Machine Learning

## Objective

Train the churn prediction model.

### Section 1: Algorithms

#### Topics

* Logistic Regression
* Decision Tree
* Random Forest
* XGBoost

**Hands-on Lab**

* Train multiple models

---

### Section 2: Evaluation

#### Topics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

**Hands-on Lab**

* Build `train.py`
* Build `evaluate.py`

---

# Module 5: FastAPI

## Objective

Expose the model through REST APIs.

### Sections

* REST APIs
* FastAPI
* Swagger
* Request Validation
* Error Handling
* Uvicorn

**Hands-on Lab**

* Build `predict.py`
* Build `api/app.py`

---

# Module 6: Containerization with Podman & Docker

## Objective

Containerize the application.

### Sections

* Docker Architecture
* Podman vs Docker
* Images
* Containers
* Dockerfile
* Containerfile
* Docker Compose

**Hands-on Lab**

* Build image
* Run locally using Podman

---

# Module 7: Kubernetes

## Objective

Deploy the application.

### Sections

* Pods
* Deployments
* Services
* ConfigMaps
* Secrets
* Ingress
* Autoscaling

**Hands-on Lab**

* Create deployment.yaml
* Create service.yaml
* Create ingress.yaml

---

# Module 8: Data Version Control (DVC)

## Objective

Version datasets and models.

### Sections

* DVC
* DVC Pipelines
* AWS S3 Remote
* Dataset Versioning
* Model Versioning

**Hands-on Lab**

* Configure DVC
* Upload to AWS S3

---

# Module 9: MLflow

## Objective

Track experiments and register models.

### Sections

* MLflow Tracking
* Experiments
* Metrics
* Artifacts
* Model Registry
* PostgreSQL Backend Store

**Hands-on Lab**

* Configure MLflow
* Compare experiments

---

# Module 10: Kubernetes Model Serving with KServe

## Objective

Deploy models using KServe.

### Sections

* KServe
* InferenceService
* Serverless Inference
* Canary Deployment
* Auto Scaling

**Hands-on Lab**

* Deploy model with KServe

---

# Module 11: Kubeflow

## Objective

Automate ML pipelines.

### Sections

* Kubeflow Architecture
* Pipelines
* Katib
* Notebook Servers
* Pipeline Automation

**Hands-on Lab**

* Create Kubeflow Pipeline

---

# Module 12: AWS MLOps

## Objective

Deploy on AWS SageMaker.

### Sections

* IAM
* S3
* EC2
* ECR
* CloudWatch
* SageMaker Studio
* Training Jobs
* Model Registry
* Real-Time Endpoints
* SageMaker Pipelines

**Hands-on Lab**

* Train and deploy the churn model on SageMaker

---

# Module 13: CI/CD & GitOps

## Objective

Automate build and deployment.

### Sections

* GitHub Actions
* Cloud Build
* Artifact Registry
* Argo CD
* GitOps
* Rollback

**Hands-on Lab**

* Build complete CI/CD pipeline

---

# Module 14: Monitoring & Observability

## Objective

Monitor infrastructure and models.

### Sections

* Prometheus
* Grafana
* Logging
* API Metrics
* Model Drift
* Data Drift

**Hands-on Lab**

* Build monitoring dashboards

---

# Module 15: Enterprise Security

## Objective

Secure the application.

### Sections

* IAM
* RBAC
* Secrets Management
* Docker Security
* Kubernetes Security
* High Availability
* Disaster Recovery

**Hands-on Lab**

* Secure Kubernetes deployment

---

# Module 16: Enterprise Capstone Project

## Objective

Build the complete production-ready platform.

### Final Deliverables

* Enterprise E-Commerce Customer Churn Prediction Platform
* GitHub Repository
* FastAPI Prediction Service
* Docker & Podman Image
* Kubernetes Deployment
* DVC Integration
* MLflow Tracking
* KServe Deployment
* Kubeflow Pipeline
* AWS SageMaker Deployment
* CI/CD Pipeline
* Prometheus & Grafana Dashboard

## Why I restructured it this way

I also changed the order slightly from the previous version:

* **FastAPI comes before DVC and MLflow**, because students first get a working application, then learn enterprise MLOps tooling.
* **Podman is introduced alongside Docker**, matching your local development environment.
* **The capstone project stays the same from the first module to the last**, so students build one continuous enterprise application instead of switching between unrelated examples. This creates a smoother learning experience and mirrors how real enterprise MLOps teams develop production systems.
