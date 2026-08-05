"""
Project Paths
Recognition System
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

PROFILES_DIR = ROOT_DIR / "storage" / "profiles"

FACES_DIR = DATA_DIR / "faces"

VOICE_DIR = DATA_DIR / "voices"

OBJECT_DIR = DATA_DIR / "objects"

EVENT_DIR = DATA_DIR / "events"


def create_project_directories():

    directories = [

        LOG_DIR,

        DATABASE_DIR,

        TEMP_DIR,

        FILES_DIR,

        PROFILES_DIR,

        FACES_DIR,

        VOICE_DIR,

        OBJECT_DIR,

        EVENT_DIR,

        MODELS_DIR,

        ASSETS_DIR,

        RESOURCES_DIR,

    ]

    for directory in directories:

        directory.mkdir(
            parents=True,
            exist_ok=True
        )