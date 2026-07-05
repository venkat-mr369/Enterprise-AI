"""
logger.py
---------
Configures structured logging for the whole application from
config/logging.yaml, falling back to a sane default if the file
or the `artifacts/` directory isn't available yet (e.g. first run).
"""

import logging
import logging.config
from pathlib import Path

import yaml

from src.config import ROOT_DIR, CONFIG_DIR, settings

_LOGGING_CONFIGURED = False


def _configure_logging() -> None:
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    settings.ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    config_path = CONFIG_DIR / "logging.yaml"
    try:
        with open(config_path, "r") as f:
            log_config = yaml.safe_load(f)
        # Make the file handler path absolute relative to project root
        file_handler = log_config.get("handlers", {}).get("file")
        if file_handler:
            file_handler["filename"] = str(ROOT_DIR / file_handler["filename"])
        logging.config.dictConfig(log_config)
    except Exception:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        )

    _LOGGING_CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-level logger, configuring logging on first use."""
    _configure_logging()
    return logging.getLogger(name)
