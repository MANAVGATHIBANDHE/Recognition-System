"""
Camera Service
Recognition System v2
"""

from core.base_service import BaseService
from core.camera.camera import Camera
from core.logger.logger import app_logger


class CameraService(BaseService):

    def __init__(self):

        super().__init__("camera")

        self.camera = Camera()

    # ---------------------------------------------------------

    def start(self) -> None:
        """
        Start camera.
        """

        if self.running:
            return

        if self.camera.open():

            self.running = True

            app_logger.success(
                "Camera Opened"
            )

        else:

            self.running = False

            app_logger.error(
                "Camera Not Found"
            )

    # ---------------------------------------------------------

    def stop(self) -> None:
        """
        Stop camera.
        """

        if not self.running:
            return

        self.camera.release()

        self.running = False

        app_logger.info(
            "Camera Released"
        )

    # ---------------------------------------------------------

    def restart(self) -> None:
        """
        Restart camera.
        """

        self.stop()

        self.start()

    # ---------------------------------------------------------

    def read(self):
        """
        Read one frame.
        """

        if not self.running:

            return False, None

        return self.camera.read()

    # ---------------------------------------------------------

    def is_available(self) -> bool:
        """
        Camera status.
        """

        return self.camera.is_open()

    # ---------------------------------------------------------

    def set_camera(self, camera_index: int):
        """
        Change camera source.
        """

        was_running = self.running

        if was_running:

            self.stop()

        self.camera = Camera(camera_index)

        if was_running:

            self.start()