import sqlite3


class PersonDatabase:

    def __init__(self):

        self.connection = sqlite3.connect(
            "storage/sqlite/recognition_system.db",
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.cursor.execute("""
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
        """)

        self.connection.commit()

    def get_all_embeddings(self):

        self.cursor.execute(
            """SELECT full_name, embedding FROM persons WHERE embedding IS NOT NULL"""
        )

        return self.cursor.fetchall()

    def get_all_persons(self):

        self.cursor.execute("""
            SELECT
                full_name,
                photo,
                relationship,
                recognition_count,
                created_at
            FROM persons
            ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    def delete_person(self, name):

        self.cursor.execute(
            """DELETE FROM persons WHERE full_name=?""",
            (name,)
        )

        self.connection.commit()


person_database = PersonDatabase()