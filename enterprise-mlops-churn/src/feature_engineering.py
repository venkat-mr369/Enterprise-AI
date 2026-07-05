"""
feature_engineering.py
------------------------
Creates derived features such as customer lifetime value (CLV)
and average monthly spend. These engineered signals typically
improve churn model performance beyond raw tenure/charges alone.
"""

import pandas as pd

from src.config import settings
from src.logger import get_logger
from src.utils import ensure_dir

logger = get_logger(__name__)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Customer Lifetime Value: a simple proxy = total charges to date
    df["CLV"] = df["TotalCharges"]

    # Average monthly spend, guarding against divide-by-zero for new customers
    df["AvgMonthlySpend"] = df["TotalCharges"] / df["tenure"].replace(0, 1)

    # Tenure bucket can help tree models split more effectively
    df["TenureYears"] = (df["tenure"] / 12).round(1)

    logger.info("Added engineered features: CLV, AvgMonthlySpend, TenureYears")
    return df


def build_and_save(df: pd.DataFrame) -> pd.DataFrame:
    df = add_features(df)
    ensure_dir(settings.PROCESSED_DATA_PATH.parent)
    df.to_csv(settings.PROCESSED_DATA_PATH, index=False)
    logger.info("Saved processed dataset to %s", settings.PROCESSED_DATA_PATH)
    return df


if __name__ == "__main__":
    from src.data_ingestion import ingest
    from src.preprocessing import preprocess

    raw = ingest()
    processed = preprocess(raw)
    featured = build_and_save(processed)
    print(featured.head())
