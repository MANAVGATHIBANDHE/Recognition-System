"""
Recognition System Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Global application configuration.
    """

    # -------------------------------------------------
    # Application
    # -------------------------------------------------

    APP_NAME = "Recognition System"

    VERSION = "2.0.0"

    BUILD = "001"

    LANGUAGE = os.getenv("LANGUAGE", "en")

    THEME = os.getenv("THEME", "dark")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # -------------------------------------------------
    # Camera
    # -------------------------------------------------

    CAMERA_INDEX = int(
        os.getenv("CAMERA_INDEX", "0")
    )

    CAMERA_WIDTH = 1280

    CAMERA_HEIGHT = 720

    CAMERA_FPS = 30

    # -------------------------------------------------
    # Recognition
    # -------------------------------------------------

    DETECTION_SIZE = (640, 640)

    RECOGNITION_THRESHOLD = 0.55

    UNKNOWN_THRESHOLD = 0.60

    TRACK_TIMEOUT = 30

    # -------------------------------------------------
    # Database
    # -------------------------------------------------

    DATABASE_NAME = "recognition_system.db"

    AUTO_SAVE = True

    # -------------------------------------------------
    # Storage
    # -------------------------------------------------

    PROFILE_FOLDER = "storage/profiles"

    UNKNOWN_FOLDER = "storage/unknown"

    EVENT_FOLDER = "storage/events"

    EXPORT_FOLDER = "storage/exports"

    LOG_FOLDER = "logs"

    # -------------------------------------------------
    # Face Crop
    # -------------------------------------------------

    FACE_PADDING = 25

    FACE_CROP_SIZE = 300