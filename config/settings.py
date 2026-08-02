"""
Recognition System Settings
"""

from dotenv import load_dotenv

load_dotenv()


class Settings:

    THEME = "dark"

    LANGUAGE = "en"

    CAMERA_INDEX = 0

    AUTO_SAVE = True

    LOG_LEVEL = "INFO"

    DATABASE_NAME = "recognition_system.db"