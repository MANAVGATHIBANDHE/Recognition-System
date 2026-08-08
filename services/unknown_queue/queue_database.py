import sqlite3
import uuid
from datetime import datetime

import numpy as np


class UnknownQueueDatabase:

    def __init__(self):

        self.connection = sqlite3.connect(
            "storage/sqlite/recognition_system.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS unknown_faces(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            uuid TEXT UNIQUE,

            photo TEXT,

            embedding BLOB,

            first_seen TEXT,

            last_seen TEXT,

            seen_count INTEGER DEFAULT 1,

            status TEXT DEFAULT 'NEW',

            camera TEXT,

            notes TEXT

        )
        """)

        self.connection.commit()

    def find_similar(
        self,
        embedding,
        threshold=0.60
    ):

        self.cursor.execute("""
            SELECT
                uuid,
                embedding
            FROM unknown_faces
        """)

        rows = self.cursor.fetchall()

        if not rows:
            return None

        embedding = embedding.astype(np.float32)

        best_uuid = None
        best_score = -1.0

        for uid, blob in rows:

            db_embedding = np.frombuffer(
                blob,
                dtype=np.float32
            )

            score = float(
                np.dot(
                    embedding,
                    db_embedding
                )
            )

            if score > best_score:
                best_score = score
                best_uuid = uid

        if best_score >= threshold:
            return best_uuid

        return None

    def add_unknown(
        self,
        photo_path,
        embedding,
        camera="Default Camera"
    ):

        uid = str(uuid.uuid4())

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute(
            """
            INSERT INTO unknown_faces(

                uuid,
                photo,
                embedding,
                first_seen,
                last_seen,
                camera

            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                uid,
                photo_path,
                embedding.astype(np.float32).tobytes(),
                now,
                now,
                camera
            )
        )

        self.connection.commit()

        return uid

    def get_all(self):

        self.cursor.execute("""
            SELECT

                uuid,

                photo,

                embedding,

                first_seen,

                last_seen,

                seen_count,

                status

            FROM unknown_faces

            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    def update_seen(
        self,
        uid
    ):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.cursor.execute(
            """
            UPDATE unknown_faces

            SET

                seen_count = seen_count + 1,

                last_seen = ?

            WHERE uuid = ?
            """,
            (
                now,
                uid
            )
        )

        self.connection.commit()

    def set_status(
        self,
        uid,
        status
    ):

        self.cursor.execute(
            """
            UPDATE unknown_faces

            SET status=?

            WHERE uuid=?
            """,
            (
                status,
                uid
            )
        )

        self.connection.commit()

    def delete(
        self,
        uid
    ):

        self.cursor.execute(
            """
            DELETE FROM unknown_faces

            WHERE uuid=?
            """,
            (
                uid,
            )
        )

        self.connection.commit()


unknown_queue_database = UnknownQueueDatabase()