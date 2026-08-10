"""
Face Tracker
Recognition System v2
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np

from config.settings import Settings
from core.logger.logger import app_logger


@dataclass
class Track:

    id: int

    embedding: np.ndarray

    last_seen: float

    bbox: tuple


class FaceTracker:

    def __init__(self):

        self.tracks = {}

        self.next_id = 1

        self.timeout = Settings.TRACK_TIMEOUT

        self.threshold = Settings.RECOGNITION_THRESHOLD

    # ==========================================================
    # REMOVE EXPIRED TRACKS
    # ==========================================================

    def cleanup(self):

        now = time.time()

        expired = []

        for track_id, track in self.tracks.items():

            if now - track.last_seen > self.timeout:

                expired.append(track_id)

        for track_id in expired:

            del self.tracks[track_id]

    # ==========================================================
    # UPDATE / CREATE TRACK
    # ==========================================================

    def update(

        self,

        embedding,

        bbox

    ):

        self.cleanup()

        embedding = embedding.astype(
            np.float32
        )

        embedding /= np.linalg.norm(
            embedding
        )

        best_track = None

        best_score = 0.0

        for track in self.tracks.values():

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

            best_score >= self.threshold

        ):

            best_track.embedding = embedding

            best_track.last_seen = time.time()

            best_track.bbox = bbox

            return best_track.id

        track = Track(

            id=self.next_id,

            embedding=embedding,

            last_seen=time.time(),

            bbox=bbox

        )

        self.tracks[track.id] = track

        self.next_id += 1

        app_logger.debug(
            f"Track Created -> {track.id}"
        )

        return track.id

    # ==========================================================
    # HELPERS
    # ==========================================================

    def get_track(

        self,

        track_id

    ):

        return self.tracks.get(track_id)

    def count(self):

        self.cleanup()

        return len(self.tracks)

    def clear(self):

        self.tracks.clear()

        self.next_id = 1

        app_logger.info(
            "Face Tracker Cleared"
        )


face_tracker = FaceTracker()