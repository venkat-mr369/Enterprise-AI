"""
preprocessing.py
-----------------
Cleans raw data and encodes categorical features. Handles the
classic Telco-style churn dataset quirks (blank TotalCharges for
brand-new customers, Yes/No flags, etc.).
"""

import pandas as pd

from src.config import settings
from src.logger import get_logger
from src.utils import yes_no_to_binary

logger = get_logger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values and coerce types."""
    df = df.copy()

    # TotalCharges can arrive as blank strings for tenure == 0 customers
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(0.0)

    df["tenure"] = df["tenure"].clip(lower=0)
    df["MonthlyCharges"] = df["MonthlyCharges"].clip(lower=0)

    logger.info("Cleaned data: %d rows remain", len(df))
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode categorical columns, binary-encode Yes/No columns."""
    df = df.copy()

    binary_cols = ["Partner", "Dependents", "PaperlessBilling"]
    for col in binary_cols:
        if col in df.columns:
            df[col] = yes_no_to_binary(df[col])

    if settings.TARGET_COLUMN in df.columns:
        df[settings.TARGET_COLUMN] = yes_no_to_binary(df[settings.TARGET_COLUMN])

    categorical_cols = [
        c for c in ["gender", "InternetService", "Contract", "PaymentMethod"]
        if c in df.columns
    ]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    logger.info("Encoded categoricals -> %d columns", df.shape[1])
    return df


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_data(df)
    df = encode_categoricals(df)
    return df


if __name__ == "__main__":
    from src.data_ingestion import ingest

    raw = ingest()
    processed = preprocess(raw)
    print(processed.head())
