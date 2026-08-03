"""
Face Service
"""

from services.face.yunet_detector import YuNetDetector
from services.face.recognizer import FaceRecognizer
from services.face.face_database import face_database


class FaceService:

    def __init__(self):

        self.detector = YuNetDetector()
        self.recognizer = FaceRecognizer()
        self.database = face_database


face_ai = FaceService()