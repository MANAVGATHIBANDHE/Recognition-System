import numpy as np

from scipy.spatial.distance import cosine
from insightface.app import FaceAnalysis

from services.face.face_database import face_database


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

    def identify(self, embedding):

        faces = face_database.get_faces()

        best_name = "Unknown"
        best_score = 0.0

        for name, image, blob in faces:

            db_embedding = np.frombuffer(
                blob,
                dtype=np.float32
            )

            score = 1 - cosine(
                embedding,
                db_embedding
            )

            if score > best_score:

                best_score = score
                best_name = name

        if best_score < 0.50:
            return "Unknown", best_score

        return best_name, best_score


face_recognizer = FaceRecognizer()