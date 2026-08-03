import sqlite3


class FaceDatabase:

    def __init__(self):

        self.connection = sqlite3.connect(
            "storage/sqlite/recognition_system.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            image TEXT,

            embedding BLOB,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.connection.commit()

    def add_face(
        self,
        name,
        image,
        embedding
    ):

        self.cursor.execute(

            """
            INSERT INTO faces(
                name,
                image,
                embedding
            )

            VALUES(
                ?,
                ?,
                ?
            )
            """,

            (
                name,
                image,
                embedding.astype("float32").tobytes()
            )

        )

        self.connection.commit()

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO faces(name, embedding)
            VALUES(?,?)
            """,
            (
                name,
                embedding.tobytes()
            )
        )

        self.connection.commit()

    def get_faces(self):

        self.cursor.execute(
            "SELECT name, image, embedding FROM faces"
        )

        return self.cursor.fetchall()

    def delete_face(self,name):

        self.cursor.execute(

            """
            DELETE FROM faces
            WHERE name=?
            """,

            (name,)
        )

        self.connection.commit()


face_database = FaceDatabase()