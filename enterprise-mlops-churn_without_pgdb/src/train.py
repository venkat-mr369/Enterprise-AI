"""
train.py
--------
Trains Random Forest and XGBoost models, tracks runs with MLflow,
and saves the best performing model (by ROC-AUC) to disk. Run this
module directly to execute the full pipeline: ingestion ->
preprocessing -> feature engineering -> train -> evaluate.

    python -m src.train
"""

import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

from src.config import settings
from src.data_ingestion import ingest
from src.evaluate import evaluate_model, save_evaluation_artifacts
from src.feature_engineering import build_and_save
from src.logger import get_logger
from src.preprocessing import preprocess
from src.utils import save_pickle

logger = get_logger(__name__)


def split_features_target(df):
    drop_cols = [settings.TARGET_COLUMN, settings.ID_COLUMN]
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y = df[settings.TARGET_COLUMN]
    return X, y


def build_models():
    rf_params = settings.MODEL_PARAMS["random_forest"]
    xgb_params = settings.MODEL_PARAMS["xgboost"]
    return {
        "random_forest": RandomForestClassifier(**rf_params),
        "xgboost": XGBClassifier(**xgb_params),
    }


def run_pipeline():
    logger.info("Starting training pipeline")

    # 1. Ingest -> 2. Preprocess -> 3. Feature engineer
    raw = ingest()
    processed = preprocess(raw)
    featured = build_and_save(processed)

    X, y = split_features_target(featured)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=settings.TEST_SIZE, random_state=settings.RANDOM_STATE,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)

    best_model = None
    best_model_name = None
    best_score = -1.0
    best_metrics = None

    for name, model in build_models().items():
        with mlflow.start_run(run_name=name):
            logger.info("Training %s", name)
            model.fit(X_train_scaled, y_train)

            metrics = evaluate_model(model, X_test_scaled, y_test)
            mlflow.log_params(model.get_params())
            mlflow.log_metrics(metrics)
            if name == "xgboost":
                mlflow.xgboost.log_model(model, artifact_path=name)
            else:
                mlflow.sklearn.log_model(model, artifact_path=name)

            logger.info("%s metrics: %s", name, metrics)

            score = metrics[settings.SELECTION_METRIC]
            if score > best_score:
                best_score = score
                best_model = model
                best_model_name = name
                best_metrics = metrics

    logger.info("Best model: %s (%s=%.4f)", best_model_name, settings.SELECTION_METRIC, best_score)

    # Persist the winning model + scaler + evaluation artifacts
    save_pickle(best_model, settings.MODEL_FILE)
    save_pickle(scaler, settings.SCALER_FILE)
    save_pickle(list(X.columns), settings.MODEL_DIR / "feature_columns.pkl")

    best_metrics["model_name"] = best_model_name
    save_evaluation_artifacts(best_model, X_test_scaled, y_test, best_metrics, list(X.columns))

    logger.info("Training pipeline complete. Model saved to %s", settings.MODEL_FILE)
    return best_model, best_metrics


if __name__ == "__main__":
    run_pipeline()
