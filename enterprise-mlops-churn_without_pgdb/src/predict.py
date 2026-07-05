"""
predict.py
----------
Loads the saved model, scaler, and feature-column list, then
performs predictions on new customer records. Used directly by
the FastAPI serving layer in api/app.py.
"""

import pandas as pd

from src.config import settings
from src.logger import get_logger
from src.preprocessing import encode_categoricals, clean_data
from src.feature_engineering import add_features
from src.utils import load_pickle

logger = get_logger(__name__)


class ChurnPredictor:
    """Wraps the trained model + preprocessing artifacts for inference."""

    def __init__(self):
        self.model = load_pickle(settings.MODEL_FILE)
        self.scaler = load_pickle(settings.SCALER_FILE)
        self.feature_columns = load_pickle(settings.MODEL_DIR / "feature_columns.pkl")
        logger.info("Loaded model, scaler, and %d feature columns", len(self.feature_columns))

    def _prepare(self, record: dict) -> pd.DataFrame:
        df = pd.DataFrame([record])

        # Run the same cleaning/encoding/feature steps used in training,
        # skipping the target column since it won't be present at inference.
        df = clean_data(df)
        df = encode_categoricals(df)
        df = add_features(df)

        # Align columns with what the model was trained on
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[self.feature_columns]
        return df

    def predict(self, record: dict) -> dict:
        X = self._prepare(record)
        X_scaled = self.scaler.transform(X)

        prediction = int(self.model.predict(X_scaled)[0])
        probability = float(self.model.predict_proba(X_scaled)[0, 1])

        return {
            "churn_prediction": "Yes" if prediction == 1 else "No",
            "churn_probability": round(probability, 4),
        }


if __name__ == "__main__":
    sample = {
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
    predictor = ChurnPredictor()
    print(predictor.predict(sample))
