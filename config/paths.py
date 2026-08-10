"""
Project Paths
Recognition System v2
"""

from pathlib import Path

# ==========================================================
# Root Directory
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# Project Folders
# ==========================================================

CONFIG_DIR = ROOT_DIR / "config"

ASSETS_DIR = ROOT_DIR / "assets"

MODELS_DIR = ROOT_DIR / "models"

LOG_DIR = ROOT_DIR / "logs"

RESOURCES_DIR = ROOT_DIR / "resources"

# ==========================================================
# Storage
# ==========================================================

STORAGE_DIR = ROOT_DIR / "storage"

DATABASE_DIR = STORAGE_DIR / "sqlite"

CACHE_DIR = STORAGE_DIR / "cache"

FILES_DIR = STORAGE_DIR / "files"

PROFILES_DIR = STORAGE_DIR / "profiles"

UNKNOWN_DIR = STORAGE_DIR / "unknown"

VOICE_DIR = STORAGE_DIR / "voices"

OBJECT_DIR = STORAGE_DIR / "objects"

EVENT_DIR = STORAGE_DIR / "events"

HISTORY_DIR = STORAGE_DIR / "history"

EXPORT_DIR = STORAGE_DIR / "exports"

TEMP_DIR = STORAGE_DIR / "temp"

# ==========================================================
# AI Model Directories
# ==========================================================

FACE_MODEL_DIR = MODELS_DIR / "buffalo_l"

YOLO_MODEL_DIR = MODELS_DIR / "yolo"

VOICE_MODEL_DIR = MODELS_DIR / "voice"

EMOTION_MODEL_DIR = MODELS_DIR / "emotion"

OCR_MODEL_DIR = MODELS_DIR / "ocr"

# ==========================================================
# Create Required Directories
# ==========================================================

def create_project_directories() -> None:
    """
    Create all required project directories.

    Safe to call multiple times.
    """

    directories = [

        LOG_DIR,

        DATABASE_DIR,

        CACHE_DIR,

        FILES_DIR,

        PROFILES_DIR,

        UNKNOWN_DIR,

        VOICE_DIR,

        OBJECT_DIR,

        EVENT_DIR,

        HISTORY_DIR,

        EXPORT_DIR,

        TEMP_DIR,

        MODELS_DIR,

        ASSETS_DIR,

        RESOURCES_DIR,

    ]

    for directory in directories:

        directory.mkdir(
            parents=True,
            exist_ok=True
        )