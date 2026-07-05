"""
evaluate.py
-----------
Calculates Accuracy, Precision, Recall, F1 Score, and ROC-AUC, and
generates evaluation artifacts (confusion matrix plot, feature
importance CSV, metrics.json) used by the API's /metrics endpoint
and by the course's model-comparison exercises.
"""

import matplotlib
matplotlib.use("Agg")  # headless rendering for containers/CI

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.config import settings
from src.logger import get_logger
from src.utils import ensure_dir, save_json

logger = get_logger(__name__)


def evaluate_model(model, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "f1_score": round(f1_score(y_test, y_pred), 4),
        "roc_auc": round(roc_auc_score(y_test, y_proba), 4),
    }
    return metrics


def save_confusion_matrix(model, X_test, y_test, path) -> None:
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["No Churn", "Churn"],
                yticklabels=["No Churn", "Churn"])
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.title("Confusion Matrix")
    plt.tight_layout()

    ensure_dir(path.parent)
    plt.savefig(path)
    plt.close()
    logger.info("Saved confusion matrix to %s", path)


def save_feature_importance(model, feature_names, path) -> None:
    if not hasattr(model, "feature_importances_"):
        logger.warning("Model has no feature_importances_, skipping")
        return

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False)

    ensure_dir(path.parent)
    importance_df.to_csv(path, index=False)
    logger.info("Saved feature importance to %s", path)


def save_evaluation_artifacts(model, X_test, y_test, metrics: dict, feature_names) -> None:
    save_json(metrics, settings.METRICS_FILE)
    save_confusion_matrix(model, X_test, y_test, settings.ARTIFACTS_DIR / "confusion_matrix.png")
    save_feature_importance(model, feature_names, settings.ARTIFACTS_DIR / "feature_importance.csv")
