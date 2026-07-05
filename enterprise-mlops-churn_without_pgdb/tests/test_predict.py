"""Unit tests for the prediction module. Requires a trained model
(run `python -m src.train` first, or rely on CI running it beforehand)."""

import pytest

from src.config import settings


@pytest.fixture(scope="module")
def predictor():
    if not settings.MODEL_FILE.exists():
        pytest.skip("Model artifacts not found; run `python -m src.train` first.")
    from src.predict import ChurnPredictor
    return ChurnPredictor()


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


def test_predict_returns_expected_keys(predictor):
    result = predictor.predict(SAMPLE_RECORD)
    assert "churn_prediction" in result
    assert "churn_probability" in result
    assert result["churn_prediction"] in {"Yes", "No"}
    assert 0.0 <= result["churn_probability"] <= 1.0


def test_predict_loyal_customer_has_lower_risk(predictor):
    loyal_customer = dict(SAMPLE_RECORD)
    loyal_customer.update({
        "tenure": 60,
        "Contract": "Two year",
        "InternetService": "DSL",
        "MonthlyCharges": 30.0,
        "TotalCharges": 1800.0,
    })
    risky_result = predictor.predict(SAMPLE_RECORD)
    loyal_result = predictor.predict(loyal_customer)
    assert loyal_result["churn_probability"] <= risky_result["churn_probability"]
