"""
Recognition System Launcher
Recognition System v2
"""

from __future__ import annotations

import sys
import traceback

from app import main
from core.logger.logger import app_logger


def launch() -> int:
    """
    Application entry point.
    """

    try:

        app_logger.info("Launching Recognition System...")

        main()

        app_logger.info("Application Closed Successfully")

        return 0

    except KeyboardInterrupt:

        app_logger.warning("Application Interrupted By User")

        return 0

    except Exception as error:

        app_logger.exception(error)

        traceback.print_exc()

        return 1


if __name__ == "__main__":

    sys.exit(
        launch()
    )