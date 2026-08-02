from core.base_service import BaseService
from core.logger.logger import app_logger

from services.face.face_detector import FaceDetector


class FaceService(BaseService):

    def __init__(self):

        super().__init__("face")

        self.detector = FaceDetector()

    def start(self):
        app_logger.success("Face AI Ready")

    def stop(self):
        app_logger.info("Face AI Stopped")