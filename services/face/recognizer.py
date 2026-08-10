"""
Face Recognizer
Recognition System v2
"""

import numpy as np

from insightface.app import FaceAnalysis

from config.settings import Settings
from core.logger.logger import app_logger
from services.person.person_database import person_database


class FaceRecognizer:

    def __init__(self):

        self.app = FaceAnalysis(
            name="buffalo_l",
            root="models"
        )

        self.app.prepare(
            ctx_id=0,
            det_size=Settings.DETECTION_SIZE
        )

        # person_name -> normalized embedding
        self.person_cache = {}

        self.reload()

    # ---------------------------------------------------------

    def start(self):

        app_logger.info(
            "Face Recognizer Running"
        )

    # ---------------------------------------------------------

    def normalize(self, embedding):

        norm = np.linalg.norm(embedding)

        if norm == 0:
            return embedding

        return embedding / norm

    # ---------------------------------------------------------

    def recognize(self, frame):

        try:

            faces = self.app.get(frame)

        except Exception as e:

            app_logger.exception(e)

            return []

        from services.tracking.tracker import face_tracker

        for face in faces:

            if not hasattr(face, "embedding"):
                continue

            if hasattr(face, "bbox"):

                bbox = tuple(
                    int(x)
                    for x in face.bbox
                )

            else:

                bbox = (0, 0, 0, 0)

            face.track_id = face_tracker.update(
                face.embedding,
                bbox
            )

        face_tracker.cleanup()

        return faces

    # ---------------------------------------------------------

    def reload(self):

        self.person_cache.clear()

        persons = person_database.get_all_embeddings()

        for name, emb_bytes in persons:

            if emb_bytes is None:
                continue

            embedding = np.frombuffer(
                emb_bytes,
                dtype=np.float32
            ).copy()

            self.person_cache[name] = self.normalize(
                embedding
            )

        app_logger.success(
            f"Loaded {len(self.person_cache)} Face Profiles"
        )

    # ---------------------------------------------------------

    def identify(self, live_embedding):

        if not self.person_cache:

            return "Unknown", 0.0

        live_embedding = self.normalize(
            live_embedding
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

        if best_score >= Settings.RECOGNITION_THRESHOLD:

            return best_name, best_score

        return "Unknown", best_score


face_recognizer = FaceRecognizer()