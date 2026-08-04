from services.face.detector import FaceDetector
from services.face.recognizer import FaceRecognizer
from services.face.trainer_old import FaceTrainer


class FaceManager:

    def __init__(self):
        self.name = "face"

        self.detector = FaceDetector()
        self.recognizer = FaceRecognizer()
        self.trainer = FaceTrainer()

    def start(self):
        self.detector.start()
        self.recognizer.start()
        self.trainer.start()

    def stop(self):
        self.detector.stop()
        self.recognizer.stop()
        self.trainer.stop()


face_service = FaceManager()