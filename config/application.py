"""
Application Configuration
"""

from version import APP_NAME, VERSION, BUILD


class ApplicationConfig:
    NAME: str = APP_NAME
    VERSION: str = VERSION
    BUILD: str = BUILD

    DEBUG: bool = False

    COMPANY: str = "Recognition System"
    ORGANIZATION: str = "Recognition AI"

    WINDOW_WIDTH: int = 1400
    WINDOW_HEIGHT: int = 850

    MIN_WIDTH: int = 1200
    MIN_HEIGHT: int = 700