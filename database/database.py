"""
Database Manager

Recognition System v2
"""

from __future__ import annotations

import sqlite3

from core.logger.logger import app_logger

from config.paths import DATABASE_DIR
from config.settings import Settings


class DatabaseManager:
    """
    SQLite Database Manager.
    """

    def __init__(self) -> None:

        DATABASE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.database_path = (
            DATABASE_DIR /
            Settings.DATABASE_NAME
        )

        self.connection: sqlite3.Connection | None = None

    # ---------------------------------------------------------

    def connect(self) -> None:
        """
        Connect to SQLite database.
        """

        if self.connection is not None:
            return

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        app_logger.success(
            f"Database Connected → {self.database_path.name}"
        )

    # ---------------------------------------------------------

    def cursor(self) -> sqlite3.Cursor:
        """
        Return database cursor.
        """

        if self.connection is None:

            raise RuntimeError(
                "Database not connected."
            )

        return self.connection.cursor()

    # ---------------------------------------------------------

    def commit(self) -> None:

        if self.connection is not None:

            self.connection.commit()

    # ---------------------------------------------------------

    def rollback(self) -> None:

        if self.connection is not None:

            self.connection.rollback()

    # ---------------------------------------------------------

    def close(self) -> None:
        """
        Close database.
        """

        if self.connection is not None:

            self.connection.close()

            self.connection = None

            app_logger.info(
                "Database Closed"
            )

    # ---------------------------------------------------------

    def create_tables(self) -> None:
        """
        Create system tables.
        """

        cursor = self.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS settings(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                key TEXT UNIQUE,

                value TEXT

            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                event TEXT,

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS system_info(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT,

                value TEXT

            )
            """
        )

        self.commit()

        app_logger.success(
            "Database Tables Ready"
        )

    # ---------------------------------------------------------

    def initialize(self) -> None:

        self.connect()

        self.create_tables()


database = DatabaseManager()