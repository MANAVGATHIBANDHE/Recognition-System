"""
Application Entry
Recognition System v2
"""

from __future__ import annotations

from application import Application


def create_application() -> Application:
    """
    Create and return the main application instance.
    """

    return Application()


def main() -> None:
    """
    Start the Recognition System.
    """

    application = create_application()

    application.run()