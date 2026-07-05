"""
config.py
---------
Centralizes paths, model settings, and application configuration.

Loads YAML files from the `config/` directory so that no module ever
hardcodes a file path or hyperparameter. This is a standard enterprise
pattern: one source of truth for configuration.
"""

from pathlib import Path
import yaml

# Project root = parent of the `src` directory
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"


def _load_yaml(filename: str) -> dict:
    path = CONFIG_DIR / filename
    with open(path, "r") as f:
        return yaml.safe_load(f)


# Load once at import time
_APP_CONFIG = _load_yaml("config.yaml")
_MODEL_CONFIG = _load_yaml("model_config.yaml")


class Settings:
    """Typed accessor around the raw config dictionaries."""

    # App
    APP_NAME = _APP_CONFIG["app"]["name"]
    APP_VERSION = _APP_CONFIG["app"]["version"]
    APP_ENV = _APP_CONFIG["app"]["env"]

    # Paths (resolved relative to project root)
    RAW_DATA_PATH = ROOT_DIR / _APP_CONFIG["paths"]["raw_data"]
    PROCESSED_DATA_PATH = ROOT_DIR / _APP_CONFIG["paths"]["processed_data"]
    MODEL_DIR = ROOT_DIR / _APP_CONFIG["paths"]["model_dir"]
    MODEL_FILE = ROOT_DIR / _APP_CONFIG["paths"]["model_file"]
    SCALER_FILE = ROOT_DIR / _APP_CONFIG["paths"]["scaler_file"]
    ARTIFACTS_DIR = ROOT_DIR / _APP_CONFIG["paths"]["artifacts_dir"]
    METRICS_FILE = ROOT_DIR / _APP_CONFIG["paths"]["metrics_file"]

    # Training
    TEST_SIZE = _APP_CONFIG["training"]["test_size"]
    RANDOM_STATE = _APP_CONFIG["training"]["random_state"]
    TARGET_COLUMN = _APP_CONFIG["training"]["target_column"]
    ID_COLUMN = _APP_CONFIG["training"]["id_column"]

    # MLflow
    MLFLOW_TRACKING_URI = _APP_CONFIG["mlflow"]["tracking_uri"]
    MLFLOW_EXPERIMENT_NAME = _APP_CONFIG["mlflow"]["experiment_name"]

    # Model hyperparameters + feature lists
    MODEL_PARAMS = _MODEL_CONFIG["models"]
    SELECTION_METRIC = _MODEL_CONFIG["selection_metric"]
    NUMERIC_FEATURES = _MODEL_CONFIG["features"]["numeric"]
    CATEGORICAL_FEATURES = _MODEL_CONFIG["features"]["categorical"]


settings = Settings()
