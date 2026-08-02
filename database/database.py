"""
Database Manager

Purpose:
    Handles SQLite database initialization and connections.

Author:
    Manav Gathibandhe

Project:
    Recognition System
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from core.logger.logger import app_logger
from config.paths import DATABASE_DIR
from config.settings import Settings


class DatabaseManager:
    """SQLite Database Manager."""

    def __init__(self) -> None:
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)

        self.database_path = DATABASE_DIR / Settings.DATABASE_NAME

        self.connection: sqlite3.Connection | None = None

    def connect(self) -> None:
        """Connect to SQLite database."""

        self.connection = sqlite3.connect(self.database_path)

        app_logger.success(
            f"Database Connected → {self.database_path.name}"
        )

    def create_tables(self) -> None:
        """Create initial application tables."""

        cursor = self.connection.cursor()

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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

        self.connection.commit()

        app_logger.success("Database Tables Ready")

    def initialize(self) -> None:
        """Initialize database."""

        self.connect()

        self.create_tables()


database = DatabaseManager()