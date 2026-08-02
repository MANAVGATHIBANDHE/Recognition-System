from insightface.app import FaceAnalysis


class FaceRecognizer:

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l",
            root="models"
        )

        self.app.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )

    def start(self):
        print("Face Recognizer Running")

    def recognize(self, frame):
        return self.app.get(frame)