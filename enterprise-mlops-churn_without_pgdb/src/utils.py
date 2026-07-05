"""
utils.py
--------
Shared helper functions used across the ingestion, training, and
serving modules. Keeping these here avoids duplicating logic.
"""

import json
from pathlib import Path
from typing import Any

import joblib


def ensure_dir(path: Path) -> None:
    """Create a directory (and parents) if it doesn't already exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def save_json(data: dict, path: Path) -> None:
    ensure_dir(Path(path).parent)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def save_pickle(obj: Any, path: Path) -> None:
    ensure_dir(Path(path).parent)
    joblib.dump(obj, path)


def load_pickle(path: Path) -> Any:
    return joblib.load(path)


def yes_no_to_binary(series):
    """Map 'Yes'/'No' style columns to 1/0."""
    return series.map({"Yes": 1, "No": 0}).astype(int)
