from core.base_service import BaseService
from core.logger.logger import app_logger


class FaceRecognizer(BaseService):

    def __init__(self):
        super().__init__("face_recognizer")

    def start(self):
        app_logger.info("Face Recognizer Running")

    def stop(self):
        app_logger.info("Face Recognizer Stopped")