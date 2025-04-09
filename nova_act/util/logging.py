"""Logging configuration module."""

import logging
from typing import Optional


def setup_logging(
    name: Optional[str] = None, level: int = logging.INFO
) -> logging.Logger:
    """Set up logging configuration.

    Args:
        name: The logger name
        level: The logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler if logger doesn't already have handlers
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

    return logger
