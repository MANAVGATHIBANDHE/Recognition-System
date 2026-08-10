"""
Person Database
Recognition System v2
"""

from __future__ import annotations

import uuid
from datetime import datetime

from database.database import database
from core.logger.logger import app_logger


class PersonDatabase:

    def __init__(self):

        database.connect()

        self.db = database

        self.create_tables()

    # ==========================================================
    # TABLES
    # ==========================================================

    def create_tables(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS persons(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                uuid TEXT UNIQUE,

                first_name TEXT,

                middle_name TEXT,

                last_name TEXT,

                full_name TEXT,

                gender TEXT,

                dob TEXT,

                phone TEXT,

                email TEXT,

                house TEXT,

                area TEXT,

                city TEXT,

                state TEXT,

                country TEXT,

                postal_code TEXT,

                occupation TEXT,

                relationship TEXT,

                tags TEXT,

                notes TEXT,

                photo TEXT,

                embedding BLOB,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                last_seen TIMESTAMP,

                recognition_count INTEGER DEFAULT 0,

                status TEXT DEFAULT 'Active'

            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS person_embeddings(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                person_uuid TEXT,

                embedding BLOB,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(person_uuid)
                REFERENCES persons(uuid)
                ON DELETE CASCADE

            )
            """
        )

        self.db.commit()

    # ==========================================================
    # PERSON CREATE
    # ==========================================================

    def create_person(

        self,

        first_name,

        middle_name,

        last_name,

        gender,

        dob,

        phone,

        email,

        house,

        area,

        city,

        state,

        country,

        postal_code,

        occupation,

        relationship,

        tags,

        notes,

        photo,

        embedding

    ):

        uid = str(uuid.uuid4())

        full_name = " ".join(

            [

                first_name,

                middle_name,

                last_name

            ]

        ).strip()

        embedding_bytes = None

        if embedding is not None:

            embedding_bytes = embedding.astype(
                "float32"
            ).tobytes()

        cursor = self.db.cursor()

        cursor.execute(

            """
            INSERT INTO persons(

                uuid,

                first_name,

                middle_name,

                last_name,

                full_name,

                gender,

                dob,

                phone,

                email,

                house,

                area,

                city,

                state,

                country,

                postal_code,

                occupation,

                relationship,

                tags,

                notes,

                photo,

                embedding

            )

            VALUES(

                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,
                ?

            )
            """,

            (

                uid,

                first_name,

                middle_name,

                last_name,

                full_name,

                gender,

                dob,

                phone,

                email,

                house,

                area,

                city,

                state,

                country,

                postal_code,

                occupation,

                relationship,

                tags,

                notes,

                photo,

                embedding_bytes

            )

        )

        if embedding_bytes is not None:

            cursor.execute(

                """
                INSERT INTO person_embeddings(

                    person_uuid,

                    embedding

                )

                VALUES(?,?)

                """,

                (

                    uid,

                    embedding_bytes

                )

            )

        self.db.commit()

        app_logger.success(

            f"Person Added -> {full_name}"

        )

        return uid

    # ==========================================================
    # EMBEDDINGS
    # ==========================================================

    def get_all_embeddings(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT
                p.full_name,
                e.embedding
            FROM person_embeddings e
            JOIN persons p
            ON p.uuid = e.person_uuid
            ORDER BY p.full_name
            """
        )

        return cursor.fetchall()

    # ----------------------------------------------------------

    def add_secondary_embedding(
        self,
        person_uuid,
        embedding_bytes
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            INSERT INTO person_embeddings(

                person_uuid,

                embedding

            )

            VALUES(?,?)

            """,
            (
                person_uuid,
                embedding_bytes
            )
        )

        self.db.commit()

    # ==========================================================
    # PERSON LOOKUP
    # ==========================================================

    def get_person_uuid(
        self,
        full_name
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT uuid

            FROM persons

            WHERE full_name=?

            """,
            (
                full_name,
            )
        )

        row = cursor.fetchone()

        if row:

            return row["uuid"]

        return None

    # ----------------------------------------------------------

    def get_person_data(
        self,
        full_name
    ):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT

                embedding,

                recognition_count

            FROM persons

            WHERE full_name=?

            """,
            (
                full_name,
            )
        )

        return cursor.fetchone()

    # ==========================================================
    # PERSON LIST
    # ==========================================================

    def get_all_persons(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT

                full_name,

                photo,

                relationship,

                recognition_count,

                created_at

            FROM persons

            ORDER BY full_name
            """
        )

        return cursor.fetchall()

    # ----------------------------------------------------------

    def get_all_persons_brief(self):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT

                full_name,

                photo,

                relationship

            FROM persons

            ORDER BY full_name
            """
        )

        return cursor.fetchall()

    # ==========================================================
    # RECOGNITION
    # ==========================================================

    def update_person_embedding(

        self,

        full_name,

        embedding_bytes,

        recognition_count

    ):

        cursor = self.db.cursor()

        cursor.execute(

            """
            UPDATE persons

            SET

                embedding=?,

                recognition_count=?,

                last_seen=?

            WHERE full_name=?

            """,

            (

                embedding_bytes,

                recognition_count,

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                full_name

            )

        )

        self.db.commit()

    # ----------------------------------------------------------

    def increment_recognition(

        self,

        full_name

    ):

        cursor = self.db.cursor()

        cursor.execute(

            """
            UPDATE persons

            SET

                recognition_count =
                recognition_count + 1,

                last_seen = ?

            WHERE full_name=?

            """,

            (

                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

                full_name

            )

        )

        self.db.commit()

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_person(

        self,

        full_name

    ):

        cursor = self.db.cursor()

        cursor.execute(

            """
            DELETE FROM persons

            WHERE full_name=?

            """,

            (
                full_name,
            )

        )

        self.db.commit()


person_database = PersonDatabase()