"""
Logger Configuration
Recognition System v2
"""

import sys

from pathlib import Path

from loguru import logger

from config.paths import LOG_DIR


# ==========================================================
# Create Log Directory
# ==========================================================

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIR / "recognition_system.log"

# ==========================================================
# Remove Default Logger
# ==========================================================

logger.remove()

# ==========================================================
# Console Logger
# ==========================================================

logger.add(

    sys.stdout,

    level="INFO",

    colorize=True,

    backtrace=True,

    diagnose=False,

    enqueue=True,

    format=(
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{name}</cyan>:"
        "<cyan>{function}</cyan>:"
        "<cyan>{line}</cyan> | "
        "{message}"
    ),
)

# ==========================================================
# File Logger
# ==========================================================

logger.add(

    LOG_FILE,

    level="DEBUG",

    rotation="10 MB",

    retention="30 days",

    compression="zip",

    encoding="utf-8",

    enqueue=True,

    backtrace=True,

    diagnose=True,

    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level:<8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)

# ==========================================================
# Global Logger
# ==========================================================

app_logger = logger