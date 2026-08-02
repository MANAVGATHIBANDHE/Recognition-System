from core.base_service import BaseService
from core.logger.logger import app_logger


class FaceDetector(BaseService):

    def __init__(self):
        super().__init__("face_detector")

    def start(self):
        app_logger.info("Face Detector Running")

    def stop(self):
        app_logger.info("Face Detector Stopped")