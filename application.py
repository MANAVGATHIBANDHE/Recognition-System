"""
Recognition System Application
"""

from config import ApplicationConfig

from core.logger.logger import app_logger
from database.database import database
from ui.themes.theme_manager import ThemeManager
from ui.windows.main_window import MainWindow

from core.service_manager import ServiceManager
from services.camera.manager import camera_service
from services.face.manager import face_service


class Application:

    def __init__(self):

        self.service_manager = ServiceManager()

    def print_banner(self):

        app_logger.info("=" * 60)
        app_logger.info(ApplicationConfig.NAME)
        app_logger.info(f"Version : {ApplicationConfig.VERSION}")
        app_logger.info(f"Build   : {ApplicationConfig.BUILD}")
        app_logger.info("=" * 60)

    def initialize(self):

        self.print_banner()

        app_logger.success("Configuration Loaded")

        app_logger.success("Logger Started")

        database.connect()

        database.create_tables()

        ThemeManager.load()

        self.service_manager.register(camera_service)

        self.service_manager.start("camera")

        self.service_manager.register(face_service)

        self.service_manager.start("face")

        app_logger.success("Recognition System Ready")

    def run(self):

        self.initialize()

        app = MainWindow()

        app.mainloop()