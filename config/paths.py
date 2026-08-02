"""
Project Paths
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"

DATA_DIR = ROOT_DIR / "data"

DATABASE_DIR = ROOT_DIR / "storage" / "sqlite"

LOG_DIR = ROOT_DIR / "logs"

MODELS_DIR = ROOT_DIR / "models"

RESOURCES_DIR = ROOT_DIR / "resources"

TEMP_DIR = ROOT_DIR / "storage" / "cache"

FILES_DIR = ROOT_DIR / "storage" / "files"