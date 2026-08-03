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

            photo TEXT,

            embedding BLOB,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            last_seen TIMESTAMP,

            recognition_count INTEGER DEFAULT 0,

            status TEXT DEFAULT 'Active'
        )
        """)

        self.connection.commit()


person_database = PersonDatabase()