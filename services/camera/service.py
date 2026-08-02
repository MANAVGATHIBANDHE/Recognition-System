"""
Camera Service
"""
from core.base_service import BaseService
from core.camera.camera import Camera
from core.logger.logger import app_logger


class CameraService(BaseService):

    def __init__(self):
        super().__init__("camera")
        self.camera = Camera()

    def start(self):

        if self.camera.open():
            app_logger.success("Camera Opened")
        else:
            app_logger.error("Camera Not Found")

    def stop(self):
        self.camera.release()
        app_logger.info("Camera Released")