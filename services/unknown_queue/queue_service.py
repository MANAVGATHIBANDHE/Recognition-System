from services.unknown_queue.queue_database import (
    unknown_queue_database
)


class UnknownQueueService:

    def __init__(self):

        self.database = unknown_queue_database

    def add(
        self,
        photo_path,
        embedding
    ):

        return self.database.add_unknown(
            photo_path,
            embedding
        )

    def get_all(self):

        return self.database.get_all()

    def delete(self, uid):

        self.database.delete(uid)

    def mark_ignored(self, uid):

        self.database.set_status(
            uid,
            "IGNORED"
        )

    def mark_pending(self, uid):

        self.database.set_status(
            uid,
            "PENDING"
        )


unknown_queue = UnknownQueueService()