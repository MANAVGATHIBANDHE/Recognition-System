"""
Face Service
"""

from core.base_service import BaseService
from services.face.yunet_detector import YuNetDetector
from services.face.recognizer import FaceRecognizer
from core.logger.logger import app_logger



class FaceService(BaseService):

    def __init__(self):

        super().__init__("face")

        self.detector = YuNetDetector()
        self.recognizer = FaceRecognizer()

    def start(self):

        self.running = True

        app_logger.success("Face Service Started")

    def stop(self):

        self.running = False

        app_logger.info("Face Service Stopped")


face_ai = FaceService()