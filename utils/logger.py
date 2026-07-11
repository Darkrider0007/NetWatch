"""
Logging utilities for NetWatch.

This module configures the application logger with:
- Console logging
- Rotating file logging
- Consistent formatting
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_DIR, LOG_FILE

LOGGER_NAME = "NetWatch"


def setup_logger() -> logging.Logger:
    """
    Configure and return the application logger.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    # Ensure log directory exists
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Rotating file handler
    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=10 * 1024 * 1024,   # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    logger.info("=" * 70)
    logger.info("NetWatch Logger Started")
    logger.info("=" * 70)

    return logger


def get_logger() -> logging.Logger:
    """
    Return the configured logger.

    If it has not been configured yet,
    configure it automatically.
    """

    logger = logging.getLogger(LOGGER_NAME)

    if not logger.handlers:
        setup_logger()

    return logger


def log_exception(exc: Exception) -> None:
    """
    Log an exception with traceback.

    Parameters
    ----------
    exc : Exception
        Exception instance.
    """

    logger = get_logger()
    logger.exception(exc)