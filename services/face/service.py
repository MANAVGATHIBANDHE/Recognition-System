"""
Face Service
"""

from core.base_service import BaseService

from services.face.yunet_detector import YuNetDetector
from services.face.recognizer import FaceRecognizer
from services.face.face_database import face_database


class FaceService(BaseService):

    def __init__(self):

        super().__init__("face")

        self.detector = YuNetDetector()
        self.recognizer = FaceRecognizer()
        self.database = face_database

    def start(self):
        print("Face Service Started")

    def stop(self):
        print("Face Service Stopped")


face_ai = FaceService()