"""
Unknown Queue Database
Recognition System v2
"""

from __future__ import annotations

import uuid
from datetime import datetime

import numpy as np

from config.settings import Settings
from core.logger.logger import app_logger
from database.database import database
from services.image.unknown_face_storage import unknown_face_storage


class UnknownQueueDatabase:

    def __init__(self):

        database.connect()

        self.db = database

        self.create_table()

    # ==========================================================
    # TABLE
    # ==========================================================

    def create_table(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
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
            """
        )

        self.db.commit()

    # ==========================================================
    # FIND SIMILAR
    # ==========================================================

    def find_similar(

        self,

        embedding

    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT

                uuid,

                embedding

            FROM unknown_faces
            """
        )

        rows = cursor.fetchall()

        if not rows:

            return None

        embedding = embedding.astype(
            np.float32
        ).copy()

        embedding /= np.linalg.norm(
            embedding
        )

        best_uuid = None

        best_score = 0.0

        for row in rows:

            db_embedding = np.frombuffer(

                row["embedding"],

                dtype=np.float32

            ).copy()

            db_embedding /= np.linalg.norm(
                db_embedding
            )

            score = float(
                np.dot(
                    embedding,
                    db_embedding
                )
            )

            if score > best_score:

                best_score = score

                best_uuid = row["uuid"]

        if best_score >= Settings.UNKNOWN_THRESHOLD:

            return best_uuid

        return None

    # ==========================================================
    # ADD UNKNOWN
    # ==========================================================

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

        cursor = self.db.cursor()

        cursor.execute(

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

                embedding.astype(
                    np.float32
                ).tobytes(),

                now,

                now,

                camera

            )

        )

        self.db.commit()

        app_logger.info(
            f"Unknown Added -> {uid}"
        )

        return uid

    # ==========================================================
    # LIST
    # ==========================================================

    def get_all(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT *

            FROM unknown_faces

            ORDER BY id DESC
            """
        )

        return cursor.fetchall()

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_seen(

        self,

        uid

    ):

        cursor = self.db.cursor()

        cursor.execute(

            """
            UPDATE unknown_faces

            SET

                seen_count = seen_count + 1,

                last_seen = ?

            WHERE uuid=?

            """,

            (

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                uid

            )

        )

        self.db.commit()

    # ==========================================================
    # STATUS
    # ==========================================================

    def set_status(

        self,

        uid,

        status

    ):

        cursor = self.db.cursor()

        cursor.execute(

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

        self.db.commit()

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(

        self,

        uid

    ):

        cursor = self.db.cursor()

        cursor.execute(

            """
            SELECT photo

            FROM unknown_faces

            WHERE uuid=?

            """,

            (

                uid,

            )

        )

        row = cursor.fetchone()

        if row:

            unknown_face_storage.delete(
                row["photo"]
            )

        cursor.execute(

            """
            DELETE FROM unknown_faces

            WHERE uuid=?

            """,

            (

                uid,

            )

        )

        self.db.commit()

        app_logger.info(
            f"Unknown Deleted -> {uid}"
        )


unknown_queue_database = UnknownQueueDatabase()