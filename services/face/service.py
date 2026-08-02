"""
Face Service
"""

from services.face.yunet_detector import YuNetDetector
from services.face.embedding import FaceEmbedding
from services.face.face_database import FaceDatabase


class FaceService:

    def __init__(self):

        self.detector = YuNetDetector()
        self.embedding = FaceEmbedding()
        self.database = FaceDatabase()


face_ai = FaceService()