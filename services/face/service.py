"""
Face Service
Recognition System v2
"""

from core.base_service import BaseService
from core.logger.logger import app_logger

from services.face.yunet_detector import YuNetDetector
from services.face.recognizer import FaceRecognizer


class FaceService(BaseService):

    def __init__(self):

        super().__init__("face")

        self.detector = YuNetDetector()

        self.recognizer = FaceRecognizer()

    # ---------------------------------------------------------

    def start(self) -> None:
        """
        Start face service.
        """

        if self.running:
            return

        self.running = True

        app_logger.success(
            "Face Service Started"
        )

    # ---------------------------------------------------------

    def stop(self) -> None:
        """
        Stop face service.
        """

        if not self.running:
            return

        self.running = False

        app_logger.info(
            "Face Service Stopped"
        )

    # ---------------------------------------------------------

    def detect(self, frame):
        """
        Detect faces.
        """

        return self.detector.detect(frame)

    # ---------------------------------------------------------

    def recognize(self, frame):
        """
        Detect + extract embeddings.
        """

        return self.recognizer.recognize(frame)

    # ---------------------------------------------------------

    def identify(self, embedding):
        """
        Identify person.
        """

        return self.recognizer.identify(
            embedding
        )

    # ---------------------------------------------------------

    def reload(self):
        """
        Reload cached embeddings.
        """

        self.recognizer.reload()


face_ai = FaceService()