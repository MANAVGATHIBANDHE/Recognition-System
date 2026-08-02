"""
Recognition System
Application Entry Point
"""

from config import ApplicationConfig

from core.logger.logger import app_logger
from database.database import database

def print_banner():

    app_logger.info("=" * 60)
    app_logger.info(ApplicationConfig.NAME)
    app_logger.info(f"Version : {ApplicationConfig.VERSION}")
    app_logger.info(f"Build   : {ApplicationConfig.BUILD}")
    app_logger.info("=" * 60)


def main():

    print_banner()

    app_logger.success("Configuration Loaded")

    app_logger.success("Logger Started")

    database.initialize()

    app_logger.success("Recognition System Ready")


if __name__ == "__main__":
    main()