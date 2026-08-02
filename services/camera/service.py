"""
Camera Service
"""

from core.base_service import BaseService
from core.logger.logger import logger


class CameraService(BaseService):

    def __init__(self):

        super().__init__("camera")

    def start(self):

        self.running = True

        logger.info("Camera Service Running")

    def stop(self):

        self.running = False

        logger.info("Camera Service Stopped")