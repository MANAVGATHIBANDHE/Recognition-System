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
            name TEXT UNIQUE,
            embedding BLOB
        )
        """)

        self.connection.commit()

    def add_face(self, name, embedding):

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
            "SELECT name, embedding FROM faces"
        )

        return self.cursor.fetchall()


face_database = FaceDatabase()