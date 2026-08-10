"""
Application Configuration
Recognition System v2
"""

from version import APP_NAME, VERSION, BUILD


class ApplicationConfig:
    """
    Global application configuration.
    """

    # ==================================================
    # APPLICATION
    # ==================================================

    NAME = APP_NAME

    VERSION = VERSION

    BUILD = BUILD

    WINDOW_TITLE = "Recognition System v2"

    COMPANY = "Recognition AI"

    ORGANIZATION = "Recognition System"

    DEBUG = False

    RELEASE_CHANNEL = "Stable"

    # ==================================================
    # WINDOW
    # ==================================================

    WINDOW_WIDTH = 1400

    WINDOW_HEIGHT = 850

    MIN_WIDTH = 1280

    MIN_HEIGHT = 720

    # ==================================================
    # DATABASE
    # ==================================================

    DATABASE_VERSION = 1

    # ==================================================
    # APPLICATION ICON
    # ==================================================

    ICON = "assets/icons/app.ico"

    # ==================================================
    # CACHE
    # ==================================================

    CACHE_SIZE = 500

    # ==================================================
    # LOGGING
    # ==================================================

    MAX_LOG_FILES = 10

    LOG_RETENTION_DAYS = 10