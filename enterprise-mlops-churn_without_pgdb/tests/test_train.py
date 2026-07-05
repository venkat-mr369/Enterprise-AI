"""Unit tests for the data + training pipeline."""

import pandas as pd
import pytest

from src.data_ingestion import DataValidationError, ingest, validate_schema
from src.feature_engineering import add_features
from src.preprocessing import clean_data, encode_categoricals


def test_ingest_returns_dataframe():
    df = ingest()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_validate_schema_raises_on_missing_columns():
    df = pd.DataFrame({"customerID": ["A"]})
    with pytest.raises(DataValidationError):
        validate_schema(df)


def test_clean_data_fills_missing_total_charges():
    df = pd.DataFrame({
        "TotalCharges": [" ", "100.5"],
        "tenure": [0, 5],
        "MonthlyCharges": [20.0, 30.0],
    })
    cleaned = clean_data(df)
    assert cleaned["TotalCharges"].iloc[0] == 0.0
    assert cleaned["TotalCharges"].iloc[1] == 100.5


def test_encode_categoricals_produces_binary_target():
    df = pd.DataFrame({
        "Partner": ["Yes", "No"],
        "Dependents": ["No", "Yes"],
        "PaperlessBilling": ["Yes", "Yes"],
        "Churn": ["Yes", "No"],
        "gender": ["Female", "Male"],
        "InternetService": ["DSL", "No"],
        "Contract": ["Month-to-month", "Two year"],
        "PaymentMethod": ["Electronic check", "Mailed check"],
    })
    encoded = encode_categoricals(df)
    assert set(encoded["Churn"].unique()) <= {0, 1}
    assert set(encoded["Partner"].unique()) <= {0, 1}


def test_add_features_creates_expected_columns():
    df = pd.DataFrame({"TotalCharges": [100.0], "tenure": [10]})
    featured = add_features(df)
    assert "CLV" in featured.columns
    assert "AvgMonthlySpend" in featured.columns
    assert "TenureYears" in featured.columns
