"""
Logger Configuration
"""

import sys

from pathlib import Path

from loguru import logger

from config.paths import LOG_DIR


LOG_DIR.mkdir(parents=True, exist_ok=True)


logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
)

logger.add(
    Path(LOG_DIR) / "recognition_system.log",
    rotation="10 MB",
    retention="10 days",
    level="DEBUG",
)

app_logger = logger