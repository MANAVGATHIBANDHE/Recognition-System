import numpy as np

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

        # person_name -> embedding ndarray
        self.person_cache = {}

        self.reload()

    def start(self):
        app_logger.info("Face Recognizer Running")

    def recognize(self, frame):

        faces = self.app.get(frame)

        from services.tracking.tracker import face_tracker

        for face in faces:

            if hasattr(face, "embedding"):

                track_id = face_tracker.update(
                    face.embedding
                )

                face.track_id = track_id

        face_tracker.cleanup()

        return faces

    def reload(self):

        self.person_cache.clear()

        persons = person_database.get_all_embeddings()

        for name, emb_bytes in persons:

            if emb_bytes is None:
                continue

            emb = np.frombuffer(
                emb_bytes,
                dtype=np.float32
            )

            emb = emb / np.linalg.norm(emb)

            self.person_cache[name] = emb

        app_logger.success(
            f"Loaded {len(self.person_cache)} Face Profiles"
        )

    def identify(self, live_embedding):

        if len(self.person_cache) == 0:
            return "Unknown", 0.0

        live_embedding = (
            live_embedding /
            np.linalg.norm(live_embedding)
        )

        best_name = "Unknown"
        best_score = 0.0

        for name, db_embedding in self.person_cache.items():

            score = float(
                np.dot(
                    live_embedding,
                    db_embedding
                )
            )

            if score > best_score:

                best_score = score
                best_name = name

        if best_score >= 0.55:
            return best_name, best_score

        return "Unknown", best_score


face_recognizer = FaceRecognizer()