"""
Recognition System Application
"""

from config import ApplicationConfig
from config.paths import create_project_directories

from core.logger.logger import app_logger
from core.service_manager import ServiceManager

from database.database import database

from ui.themes.theme_manager import ThemeManager
from ui.windows.main_window import MainWindow

from services.camera.manager import camera_service
from services.face.service import face_ai


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

        app_logger.info("Initializing application...")

        create_project_directories()

        app_logger.success("Project directories ready.")

        app_logger.success("Logger Started")

        database.connect()

        database.create_tables()

        app_logger.success("Database Ready")

        ThemeManager.load()

        app_logger.success("Theme Loaded")

        # -----------------------------
        # Register Services
        # -----------------------------

        self.service_manager.register(camera_service)
        self.service_manager.register(face_ai)

        # -----------------------------
        # Start Services
        # -----------------------------

        self.service_manager.start_all()

        app_logger.success(
            "Recognition System Ready"
        )

    def shutdown(self):

        app_logger.info("Stopping services...")

        self.service_manager.stop_all()

        database.close()

        app_logger.success(
            "Application Closed"
        )

    def run(self):

        try:

            self.initialize()

            app = MainWindow()

            app.protocol(
                "WM_DELETE_WINDOW",
                lambda: (
                    self.shutdown(),
                    app.destroy()
                )
            )

            app.mainloop()

        except Exception as e:

            app_logger.exception(e)

            self.shutdown()