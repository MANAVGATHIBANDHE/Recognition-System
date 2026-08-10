"""
Unknown Queue Service
Recognition System v2
"""

from core.logger.logger import app_logger

from services.image.unknown_face_storage import (
    unknown_face_storage,
)

from services.unknown_queue.queue_database import (
    unknown_queue_database,
)


class UnknownQueueService:

    def __init__(self):

        self.database = unknown_queue_database

    # ==========================================================
    # ADD UNKNOWN
    # ==========================================================

    def add(

        self,

        image,

        embedding

    ):

        if image is None:

            return None

        if embedding is None:

            return None

        uid = self.database.find_similar(
            embedding
        )

        if uid:

            self.database.update_seen(uid)

            app_logger.info(
                f"Unknown Updated -> {uid}"
            )

            return uid

        photo = unknown_face_storage.save(
            image
        )

        if photo is None:

            return None

        uid = self.database.add_unknown(

            photo,

            embedding

        )

        app_logger.info(
            f"Unknown Added -> {uid}"
        )

        return uid

    # ==========================================================
    # LIST
    # ==========================================================

    def get_all(self):

        return self.database.get_all()

    def count(self):

        return len(
            self.database.get_all()
        )

    # ==========================================================
    # STATUS
    # ==========================================================

    def mark_ignored(

        self,

        uid

    ):

        self.database.set_status(

            uid,

            "IGNORED"

        )

        app_logger.info(
            f"Ignored -> {uid}"
        )

    def mark_pending(

        self,

        uid

    ):

        self.database.set_status(

            uid,

            "PENDING"

        )

    def mark_registered(

        self,

        uid

    ):

        self.database.set_status(

            uid,

            "REGISTERED"

        )

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(

        self,

        uid

    ):

        self.database.delete(uid)

        app_logger.info(
            f"Deleted Unknown -> {uid}"
        )


unknown_queue = UnknownQueueService()