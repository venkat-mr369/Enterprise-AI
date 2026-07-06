**Sanofi** or **Pfizer**, this is actually a very realistic **MLOps use case**. 
It demonstrates Data Science, ML Engineering, API development, and MLOps in one end-to-end project.

---

# Enterprise Healthcare MLOps Project

## Project Name

**Cancer Vaccine Eligibility Prediction System**

**Business Problem**

A pharmaceutical company manufactures a preventive cancer vaccine.

Hospitals upload patient records every day.

The company wants an AI model that predicts whether a patient should be recommended for the vaccine based on medical guidelines.

The prediction should be available instantly to hospital applications through a REST API.

Every prediction should be stored for auditing and monitoring.

---

# Overall Architecture

```
Hospital A
        \
Hospital B -----> Central EMR Database
        /
Hospital C

          │
          ▼
     Data Engineering
 (Cleaning & Validation)

          │
          ▼
   Feature Engineering

          │
          ▼
      ML Model Training

          │
          ▼
     Model Validation

          │
          ▼
    Model Registry

          │
          ▼
 REST API (FastAPI)

          │
          ▼
 Kubernetes Deployment

          │
          ▼
 Hospital Applications

          │
          ▼
Prediction Logs

          │
          ▼
Monitoring Dashboard
```

---

# Step 1 Hospital Database

Every hospital inserts patient data.

Example table

```
patients
```

| patient_id | name | age | gender | height_cm | weight_kg | bmi | family_history | diabetes | smoking | vaccine_taken |
| ---------- | ---- | --- | ------ | --------- | --------- | --- | -------------- | -------- | ------- | ------------- |

---

Example

```
1001
John
48
Male
170
90
31.1
Yes
Yes
No
No
```

---

# Step 2 Data Science

Data Scientist extracts data.

```
SELECT *
FROM patients;
```

Load into Pandas.

```
df = pd.read_sql(...)
```

---

# Step 3 Data Cleaning

Remove

Missing values

Duplicate patients

Incorrect ages

Negative weights

Wrong BMI

---

Calculate BMI

```
BMI =
Weight
-------------
Height²
```

Python

```
BMI = weight / (height * height)
```

---

# Step 4 Feature Engineering

Features

```
Age

Gender

BMI

Smoking

Diabetes

Family History

Blood Pressure

Cholesterol

Previous Diseases
```

Target

```
Need Vaccine

Yes

No
```

---

# Business Rule

Example

```
BMI >=30

AND

Age >=40

AND

Family History = Yes

↓

Recommend Vaccine
```

This rule can be used to generate labels for training data, or clinicians can provide the labels if available.

---

# Step 5 Model Training

Train

Random Forest

```
X =

Age
BMI
Smoking
Family History
Diabetes
```

```
y

Need Vaccine
```

```
RandomForestClassifier()
```

Output

```
Model Accuracy

95%
```

---

# Step 6 Save Model

```
model.pkl
```

or

```
joblib.dump()
```

---

# Step 7 Model Registry

Register

```
Cancer_Vaccine_Model

Version 1
```

Store

Version

Accuracy

Author

Training Date

Metrics

Approval Status

---

# Step 8 REST API

FastAPI

```
POST

/predict
```

Input

```json
{
  "age": 48,
  "bmi": 31.4,
  "diabetes": 1,
  "smoking": 0,
  "family_history": 1
}
```

Prediction

```json
{
   "recommendation":"Eligible",
   "confidence":0.96
}
```

---

# Hospital Workflow

Doctor enters patient details.

↓

Hospital application calls REST API.

↓

AI predicts.

↓

Doctor sees

```
Recommend Vaccine
```

or

```
Not Required
```

---

# Step 9 Docker

Package API.

```
Dockerfile
```

↓

Build

```
docker build
```

↓

Push

```
Artifact Registry

Docker Hub
```

---

# Step 10 CI/CD

GitHub

↓

Push Code

↓

GitHub Actions

↓

Run Unit Tests

↓

Build Docker Image

↓

Push Image

↓

Deploy to Kubernetes

---

# Step 11 Kubernetes

Deployment

```
replicas=3
```

Service

```
LoadBalancer
```

Ingress

```
/predict
```

Hospital applications call

```
https://vaccine.company.com/predict
```

---

# Step 12 Monitoring

Prometheus

Collect

API Requests

Latency

Prediction Count

CPU

Memory

---

Grafana Dashboard

Shows

```
Hospital Wise Requests

Successful Predictions

Failed Predictions

Average Response Time

API Availability
```

---

# Step 13 Prediction Logging

Every API request is saved.

Table

```
prediction_logs
```

|Patient ID|Prediction|Confidence|Doctor|Hospital|Timestamp|

This supports auditing and regulatory compliance.

---

# Step 14 Model Monitoring

Monitor

Accuracy

Prediction Drift

Feature Drift

False Predictions

If performance drops below a threshold, retrain the model with new hospital data.

---

# End-to-End Example

A patient visits **Apollo Hospital**.

The doctor enters:

* Age = 45
* Height = 170 cm
* Weight = 92 kg
* BMI = 31.8
* Family History = Yes
* Diabetes = Yes
* Smoking = No

The hospital application sends these details to the `/predict` REST API.

The model returns:

```json
{
  "recommendation": "Eligible",
  "confidence": 0.97
}
```

The doctor sees the recommendation and decides whether to administer the vaccine according to clinical protocols.

The prediction is stored in `prediction_logs`, monitored by Prometheus and Grafana, and included in future model retraining after review.

---

## Technology Stack

* **Database:** PostgreSQL
* **Data Processing:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (Random Forest)
* **API:** FastAPI
* **Containerization:** Docker
* **Version Control:** GitHub
* **CI/CD:** GitHub Actions or Jenkins
* **Model Registry:** MLflow
* **Orchestration:** Kubernetes
* **Monitoring:** Prometheus + Grafana
* **Logging:** PostgreSQL + ELK (optional)

One important note: in a real healthcare environment, a rule such as **"BMI ≥ 30 ⇒ give the vaccine"** would not be used by itself. 
Vaccine recommendations are based on approved clinical guidelines, regulatory requirements, and physician judgment. 

### Project Title

**AI-Based Cancer Vaccine Eligibility Prediction using MLOps**

### Duration

**45 Days** (60–75 minutes per day)

### What students will build

By the end of the course, students will build a complete enterprise application:

* Enterprise PostgreSQL database
* Hospital patient management system
* Data Science model (Scikit-learn)
* FastAPI REST API
* MLflow Model Registry
* Docker container
* Kubernetes deployment
* GitHub Actions CI/CD pipeline
* Prometheus & Grafana monitoring
* Complete MLOps pipeline

### Enterprise Workflow

```
Hospital Registration
        │
        ▼
Patient Visits Hospital
        │
        ▼
Doctor Records Patient Details
        │
        ▼
PostgreSQL Database
        │
        ▼
Data Cleaning & Feature Engineering
        │
        ▼
Train ML Model
        │
        ▼
MLflow Model Registry
        │
        ▼
FastAPI Prediction Service
        │
        ▼
Docker Image
        │
        ▼
GitHub Actions CI/CD
        │
        ▼
Kubernetes Deployment
        │
        ▼
Hospital Application Uses API
        │
        ▼
Prediction Logs
        │
        ▼
Prometheus + Grafana Monitoring
```

### Realistic Database

We will create around **10 relational tables**, including:

1. hospitals
2. doctors
3. patients
4. patient_visits
5. vaccinations
6. lab_reports
7. diagnoses
8. prediction_logs
9. model_versions
10. audit_logs

### Sample Prediction Logic

Input:

* Age
* Height
* Weight
* BMI
* Family History
* Smoking
* Diabetes
* Blood Pressure
* Cholesterol

Output:

* **Eligible for Vaccine**
* **Not Eligible**
* Confidence Score

### Technologies

* PostgreSQL
* Python
* Pandas
* NumPy
* Scikit-learn
* FastAPI
* MLflow
* Docker
* GitHub
* GitHub Actions
* Kubernetes
* Prometheus
* Grafana

### Deliverables

I'll prepare everything professionally:

* Enterprise PostgreSQL schema and SQL scripts
* Sample CSV datasets (10,000+ patient records)
* Data cleaning notebook
* Feature engineering notebook
* Model training notebook
* MLflow integration
* FastAPI application
* Dockerfile
* Kubernetes YAML files
* GitHub Actions CI/CD pipeline
* Prometheus & Grafana configuration
* End-to-end project documentation
* Architecture diagrams
* Interview questions based on the project

This will be a complete enterprise MLOps project suitable for training, demos, and interviews.
