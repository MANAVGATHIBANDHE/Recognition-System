from services.unknown_queue.queue_database import (
    unknown_queue_database
)

from services.image.unknown_face_storage import (
    unknown_face_storage
)


class UnknownQueueService:

    def __init__(self):

        self.database = unknown_queue_database

    def add(
        self,
        image,
        embedding
    ):

        uid = self.database.find_similar(
            embedding
        )

        if uid:

            self.database.update_seen(uid)

            return uid

        photo_path = unknown_face_storage.save(
            image
        )

        return self.database.add_unknown(
            photo_path,
            embedding
        )

    def get_all(self):

        return self.database.get_all()

    def delete(
        self,
        uid
    ):

        self.database.delete(uid)

    def mark_ignored(
        self,
        uid
    ):

        self.database.set_status(
            uid,
            "IGNORED"
        )

    def mark_pending(
        self,
        uid
    ):

        self.database.set_status(
            uid,
            "PENDING"
        )


unknown_queue = UnknownQueueService()