"""Integration tests for the FastAPI serving layer."""

import pytest
from fastapi.testclient import TestClient

from api.app import app
from src.config import settings

SAMPLE_RECORD = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 5,
    "InternetService": "Fiber optic",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 85.5,
    "TotalCharges": 427.5,
}


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert "model_loaded" in response.json()


def test_predict(client):
    if not settings.MODEL_FILE.exists():
        pytest.skip("Model artifacts not found; run `python -m src.train` first.")
    response = client.post("/predict", json=SAMPLE_RECORD)
    assert response.status_code == 200
    body = response.json()
    assert body["churn_prediction"] in {"Yes", "No"}


def test_metrics(client):
    if not settings.METRICS_FILE.exists():
        pytest.skip("Metrics not found; run `python -m src.train` first.")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "roc_auc" in response.json()
