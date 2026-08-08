from dataclasses import dataclass
import time
import numpy as np


@dataclass
class Track:

    id: int

    embedding: np.ndarray

    last_seen: float

    missed: int = 0


class FaceTracker:

    def __init__(self):

        self.next_id = 1

        self.tracks = []

        self.similarity_threshold = 0.70

        self.max_missed = 15

    def update(self, embedding):

        embedding = embedding.astype("float32")

        embedding = embedding / np.linalg.norm(embedding)

        best_track = None

        best_score = -1

        for track in self.tracks:

            score = float(
                np.dot(
                    embedding,
                    track.embedding
                )
            )

            if score > best_score:

                best_score = score

                best_track = track

        if (
            best_track is not None
            and
            best_score >= self.similarity_threshold
        ):

            best_track.embedding = embedding

            best_track.last_seen = time.time()

            best_track.missed = 0

            return best_track.id

        track = Track(

            id=self.next_id,

            embedding=embedding,

            last_seen=time.time()

        )

        self.tracks.append(track)

        self.next_id += 1

        return track.id

    def cleanup(self):

        now = time.time()

        alive = []

        for track in self.tracks:

            if now - track.last_seen < 2:

                alive.append(track)

        self.tracks = alive


face_tracker = FaceTracker()