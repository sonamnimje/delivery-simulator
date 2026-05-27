"""
Logger configuration using Loguru.
Sets up structured logging for the application.
"""

import sys
from pathlib import Path

from loguru import logger

from .config import get_settings


def setup_logger():
    """
    Configure logger with file and console handlers.
    Sets appropriate log levels and formats.
    """
    settings = get_settings()

    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stdout,
        format=settings.log_format,
        level=settings.log_level,
        colorize=True,
    )

    # File handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        format=settings.log_format,
        level=settings.log_level,
        rotation="00:00",  # Rotate daily
        retention="7 days",
    )

    logger.add(
        log_dir / "errors_{time:YYYY-MM-DD}.log",
        format=settings.log_format,
        level="ERROR",
        rotation="00:00",
        retention="30 days",
    )

    logger.info(f"Logger initialized - Level: {settings.log_level}")


# Initialize logger on import
setup_logger()
