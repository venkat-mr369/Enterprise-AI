"""
data_ingestion.py
------------------
Loads the raw CSV and validates it before it enters the pipeline.
In an enterprise setting this is where you'd also pull from a
warehouse (BigQuery/Snowflake), an S3 bucket, or a feature store.
"""

import pandas as pd

from src.config import settings
from src.logger import get_logger

logger = get_logger(__name__)

REQUIRED_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "InternetService",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]


class DataValidationError(Exception):
    """Raised when the raw dataset fails schema validation."""


def load_raw_data(path=None) -> pd.DataFrame:
    """Load the raw churn CSV from disk."""
    path = path or settings.RAW_DATA_PATH
    logger.info("Loading raw data from %s", path)
    df = pd.read_csv(path)
    logger.info("Loaded %d rows, %d columns", *df.shape)
    return df


def validate_schema(df: pd.DataFrame) -> None:
    """Fail fast if expected columns are missing."""
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise DataValidationError(f"Missing required columns: {sorted(missing)}")

    if df[settings.ID_COLUMN].duplicated().any():
        raise DataValidationError("Duplicate customerID values found in raw data")

    logger.info("Schema validation passed")


def ingest() -> pd.DataFrame:
    """Full ingestion step: load + validate."""
    df = load_raw_data()
    validate_schema(df)
    return df


if __name__ == "__main__":
    data = ingest()
    print(data.head())
