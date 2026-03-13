"""Centralized logging configuration."""

import logging
import os
import sys

from pythonjsonlogger import jsonlogger


def setup_logging() -> logging.Logger:
    """Configure and return the root application logger.

    Reads LOG_LEVEL from environment (default: INFO).
    Outputs structured JSON logs to stderr.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger("app")
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.debug("Logging initialized", extra={"log_level": log_level})
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a child logger with the given name.

    Args:
        name: Logger name, typically the module name (e.g. 'calendar_client').

    Returns:
        A child logger under the 'app' namespace.
    """
    return logging.getLogger(f"app.{name}")
