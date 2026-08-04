import numpy as np

from scipy.spatial.distance import cosine
from insightface.app import FaceAnalysis
from services.person.person_database import person_database
from core.logger.logger import app_logger


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

        self.persons = []

        self.reload()

    def start(self):
        app_logger.info("Face Recognizer Running")

    def recognize(self, frame):
        return self.app.get(frame)

    def identify(self, live_embedding):

        persons = self.persons

        if len(persons) == 0:
            return "Unknown", 0.0

        best_name = "Unknown"
        best_score = 0.0

        for name, db_bytes in persons:

            if db_bytes is None:
                continue

            db_embedding = np.frombuffer(
                db_bytes,
                dtype=np.float32
            )

            score = np.dot(
                live_embedding,
                db_embedding
            ) / (
                np.linalg.norm(live_embedding)
                * np.linalg.norm(db_embedding)
            )

            if score > best_score:

                best_score = score
                best_name = name

        if best_score >= 0.55:
            return best_name, float(best_score)

        return "Unknown", float(best_score)

    def reload(self):

        self.persons = person_database.get_all_embeddings()


face_recognizer = FaceRecognizer()