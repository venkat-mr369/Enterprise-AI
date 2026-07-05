# Module 1 – Introduction to Enterprise MLOps

**Capstone Project**

> Enterprise Customer Churn Prediction using MLOps

Industry

* E-commerce

Business Problem

Predict customers who are likely to stop purchasing so the business can proactively retain them using discounts, loyalty rewards, or personalized offers.

Technology Stack

* Python
* Git & GitHub
* VS Code
* Docker
* MLflow
* DVC
* FastAPI
* PostgreSQL
* Kubernetes
* Jenkins/GitHub Actions
* Prometheus
* Grafana
* GCP (later modules)

---

# Learning Objectives

After completing this module, students will be able to

* Understand AI, ML and Deep Learning
* Understand enterprise ML lifecycle
* Explain MLOps
* Understand why organizations use MLOps
* Set up development environment
* Create first Git repository
* Write first Python program
* Prepare environment for future labs

---

# 1. What is Artificial Intelligence (AI)?

Artificial Intelligence is the science of building systems capable of performing tasks that normally require human intelligence.

Examples

* Face Recognition
* Voice Assistants
* Self-driving Cars
* Fraud Detection
* Recommendation Systems
* Chatbots

Example in Ecommerce

Amazon recommends products based on your browsing history.

AI is the broadest field.

```
Artificial Intelligence

├── Machine Learning

│ ├── Deep Learning

│ └── Traditional ML

└── Expert Systems
```

---

# 2. What is Machine Learning?

Machine Learning is a subset of AI where computers learn patterns from data instead of being explicitly programmed.

Instead of

```
IF customer spent >10000
THEN VIP
```

ML learns

```
Past customer data

↓

Learns patterns

↓

Predicts future customer behavior
```

Example

Customer

Age = 32

Orders = 15

Last Purchase = 90 days

Average Spend = ₹850

Prediction

Likely to Churn = Yes

---

# 3. What is Deep Learning?

Deep Learning is a subset of Machine Learning that uses Neural Networks.

Used for

* Images
* Video
* Speech
* NLP
* Large Language Models

Examples

* ChatGPT
* Face Detection
* Autonomous Driving

---

# AI vs ML vs DL

| AI                 | ML               | DL                           |
| ------------------ | ---------------- | ---------------------------- |
| Broad concept      | Learns from data | Learns using neural networks |
| Can use rules      | Uses algorithms  | Uses deep neural networks    |
| Less data required | Medium data      | Huge data                    |
| Examples: Chatbot  | Customer Churn   | Image Recognition            |

---

# Types of Machine Learning

## Supervised Learning

Uses labeled data.

Example

| Customer | Churn |
| -------- | ----- |
| Ravi     | Yes   |
| John     | No    |

Algorithms

* Linear Regression
* Logistic Regression
* Random Forest
* XGBoost

Our project

Customer Churn Prediction

is

Supervised Learning

---

## Unsupervised Learning

No labels.

Goal

Find hidden patterns.

Examples

* Customer Segmentation
* Market Basket Analysis
* Product Clustering

Algorithms

* K-Means
* DBSCAN
* Hierarchical Clustering

---

## Reinforcement Learning

Agent learns by rewards.

Examples

* Robotics
* Self Driving Cars
* Games
* Dynamic Pricing

---

# Real-world ML Use Cases

Healthcare

* Disease Prediction

Finance

* Fraud Detection

Insurance

* Claim Prediction

Manufacturing

* Predictive Maintenance

Retail

* Recommendation System

Telecom

* Customer Churn

Ecommerce

* Customer Lifetime Value
* Product Recommendation
* Customer Churn Prediction
* Dynamic Pricing
* Inventory Forecasting

---

# Enterprise ML Lifecycle

```
Business Problem

↓

Data Collection

↓

Data Validation

↓

EDA

↓

Feature Engineering

↓

Model Training

↓

Model Evaluation

↓

Model Deployment

↓

Monitoring

↓

Retraining
```

---

## Our Capstone Lifecycle

Business Problem

↓

Customer Purchase Dataset

↓

Cleaning

↓

Feature Engineering

↓

Train XGBoost

↓

MLflow

↓

Deploy API

↓

Docker

↓

Kubernetes

↓

Monitoring

↓

Retrain

---

# Traditional ML vs MLOps

Traditional ML

```
Notebook

↓

Train Model

↓

Save Model

↓

Done
```

Enterprise MLOps

```
Git

↓

CI/CD

↓

Docker

↓

MLflow

↓

Testing

↓

Deployment

↓

Monitoring

↓

Retraining
```

| Traditional ML  | Enterprise MLOps      |
| --------------- | --------------------- |
| Manual          | Automated             |
| Local           | Cloud                 |
| No versioning   | Version control       |
| No monitoring   | Continuous monitoring |
| Hard deployment | Automated deployment  |

---

# What is MLOps?

MLOps

Machine Learning Operations

Combination of

* Machine Learning
* DevOps
* Data Engineering

Purpose

Deploy ML models reliably into production.

Pipeline

```
Data

↓

Training

↓

Validation

↓

Versioning

↓

Deployment

↓

Monitoring

↓

Retraining
```

---

# Why Organizations Need MLOps

Problems

* Models degrade
* Data changes
* Manual deployment
* No monitoring
* Difficult rollback

Benefits

* Faster deployment
* Better collaboration
* Reproducibility
* Version control
* Monitoring
* Automated retraining
* Compliance

---

# Roles of an MLOps Engineer

Responsibilities

* Build ML pipelines
* Automate deployments
* Docker containers
* Kubernetes
* CI/CD
* MLflow
* Monitoring
* Infrastructure
* Security
* Logging

---

# Enterprise MLOps Architecture

```
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

                  MLflow Tracking

                        │

                        ▼

                 Model Registry

                        │

                        ▼

                  Docker Image

                        │

                        ▼

                  Kubernetes

                        │

                        ▼

                 FastAPI Service

                        │

                        ▼

             Prometheus + Grafana

                        │

                        ▼

                  Model Monitoring

                        │

                        ▼

                  Automated Retraining
```

---

# Capstone Project Overview

Project Name

Enterprise Customer Churn Prediction using MLOps

Goal

Predict whether a customer will leave the platform.

Dataset Columns

* CustomerID
* Gender
* Age
* City
* Membership
* Orders
* TotalSpend
* LastPurchaseDays
* CouponsUsed
* AvgOrderValue
* Returns
* SupportTickets
* PaymentMode
* Churn

Target

```
Churn

0 = Active Customer

1 = Churned Customer
```

---

# LAB 1 — Development Environment Setup

## Lab Objective

Prepare a professional MLOps development environment for the Customer Churn project.

### Prerequisites

* Windows 10/11, macOS, or Linux
* Internet connection
* Administrator access

---

## Step 1: Install Python

1. Download the latest stable Python 3.12.x from the official website.
2. During installation, check **"Add Python to PATH"**.
3. Complete the installation.

Verify:

```bash
python --version
```

or

```bash
python3 --version
```

Expected:

```text
Python 3.12.x
```

Check pip:

```bash
pip --version
```

---

## Step 2: Create Project Folder

```bash
mkdir ecommerce-churn-mlops
cd ecommerce-churn-mlops
```

---

## Step 3: Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Verify:

```bash
which python
```

or (Windows):

```cmd
where python
```

The path should point to the virtual environment.

---

## Step 4: Upgrade pip

```bash
python -m pip install --upgrade pip
```

Verify:

```bash
pip --version
```

---

## Step 5: Install VS Code

1. Download Visual Studio Code from the official website.
2. Install it using default settings.
3. Enable **Add to PATH** if prompted.

Verify:

```bash
code --version
```

If the command is unavailable, open VS Code once and install the shell command from the Command Palette if needed.

---

## Step 6: Install Recommended VS Code Extensions

* Python
* Pylance
* Jupyter
* GitLens
* Docker
* YAML
* Markdown All in One
* GitHub Pull Requests and Issues

---

## Step 7: Open the Project

```bash
code .
```

---

## Step 8: Create Initial Project Structure

```text
ecommerce-churn-mlops/
│
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── models/
├── configs/
├── tests/
├── docs/
├── .gitignore
├── README.md
└── requirements.txt
```

Create directories:

```bash
mkdir data data/raw data/processed notebooks src models configs tests docs
```

---

## Step 9: Create `requirements.txt`

Initial dependencies:

```text
pandas
numpy
scikit-learn
matplotlib
jupyter
ipykernel
```

Install:

```bash
pip install -r requirements.txt
```

Freeze versions:

```bash
pip freeze > requirements-lock.txt
```

---

## Step 10: Create a GitHub Repository

1. Sign in to GitHub.
2. Click **New Repository**.
3. Repository name: `ecommerce-churn-mlops`
4. Add a `README.md`.
5. Create the repository.

---

## Step 11: Initialize Git Locally

```bash
git init
git add .
git commit -m "Initial project structure"
```

Add the remote repository:

```bash
git remote add origin <your-github-repository-url>
git branch -M main
git push -u origin main
```

Verify:

```bash
git remote -v
git status
```

---

## Step 12: Verify the Environment

Create `hello.py`:

```python
print("Enterprise MLOps Lab is Ready!")
```

Run:

```bash
python hello.py
```

Expected output:

```text
Enterprise MLOps Lab is Ready!
```

---

# Module Summary

By the end of this module, you should be able to:

* Explain the differences between AI, ML, and Deep Learning.
* Describe supervised, unsupervised, and reinforcement learning with e-commerce examples.
* Understand the enterprise ML lifecycle and why MLOps is essential.
* Describe the role of an MLOps engineer and an enterprise MLOps architecture.
* Set up a Python development environment with a virtual environment.
* Install and configure VS Code with recommended extensions.
* Initialize a GitHub repository and local Git project.
* Create a professional project structure for the **Enterprise Customer Churn Prediction** capstone.


