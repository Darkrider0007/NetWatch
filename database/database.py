"""
SQLite database module for NetWatch.

Responsible for:
- Database initialization
- Table creation
- Inserting connection history
- Reading history
- Clearing history
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from config import DATABASE_PATH
from utils.logger import get_logger

logger = get_logger()


CONNECTIONS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS connections
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    time TEXT NOT NULL,

    process TEXT,

    publisher TEXT,

    pid INTEGER,

    protocol TEXT,

    local_ip TEXT,

    local_port INTEGER,

    remote_ip TEXT,

    remote_port INTEGER,

    remote_host TEXT,

    country TEXT,

    status TEXT,

    bytes_sent INTEGER DEFAULT 0,

    bytes_received INTEGER DEFAULT 0
)
"""


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite connection.
    """

    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """
    Create database tables if they do not exist.
    """

    logger.info("Initializing database...")

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            CONNECTIONS_TABLE_SCHEMA
        )

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'connection_history'
            """
        )

        has_legacy_history = cursor.fetchone() is not None

        if has_legacy_history:
            cursor.execute("SELECT COUNT(*) FROM connections")
            has_connections_rows = cursor.fetchone()[0] > 0

            if not has_connections_rows:
                cursor.execute(
                    """
                    INSERT INTO connections
                    (
                        time,
                        process,
                        publisher,
                        pid,
                        protocol,
                        local_ip,
                        local_port,
                        remote_ip,
                        remote_port,
                        remote_host,
                        country,
                        status,
                        bytes_sent,
                        bytes_received
                    )
                    SELECT
                        timestamp,
                        process_name,
                        '',
                        pid,
                        protocol,
                        local_address,
                        local_port,
                        remote_address,
                        remote_port,
                        '',
                        '',
                        status,
                        bytes_sent,
                        bytes_received
                    FROM connection_history
                    """
                )

        connection.commit()

    logger.info("Database initialized successfully.")


def insert_connection(
    timestamp: str,
    process_name: str,
    pid: int,
    protocol: str,
    local_address: str,
    local_port: int,
    remote_address: str,
    remote_port: int,
    status: str,
    bytes_sent: int = 0,
    bytes_received: int = 0,
) -> None:
    """
    Insert a connection record into the database.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO connections
            (
                time,
                process,
                publisher,
                pid,
                protocol,
                local_ip,
                local_port,
                remote_ip,
                remote_port,
                remote_host,
                country,
                status,
                bytes_sent,
                bytes_received
            )

            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,?
            )
            """,
            (
                timestamp,
                process_name,
                "",
                pid,
                protocol,
                local_address,
                local_port,
                remote_address,
                remote_port,
                "",
                "",
                status,
                bytes_sent,
                bytes_received,
            ),
        )

        connection.commit()


def get_history(limit: int = 500) -> list[dict[str, Any]]:
    """
    Retrieve recent connection history.

    Parameters
    ----------
    limit : int
        Maximum rows returned.

    Returns
    -------
    list
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM connections

            ORDER BY id DESC

            LIMIT ?
            """,
            (limit,),
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def search_process(process_name: str) -> list[dict[str, Any]]:
    """
    Search history by process name.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM connections

            WHERE process LIKE ?

            ORDER BY id DESC
            """,
            (f"%{process_name}%",),
        )

        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def clear_history() -> None:
    """
    Delete all connection history.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM connections
            """
        )

        connection.commit()

    logger.warning("Connection history cleared.")


def get_total_records() -> int:
    """
    Return total number of records.
    """

    with get_connection() as connection:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM connections
            """
        )

        count = cursor.fetchone()[0]

    return count


def vacuum_database() -> None:
    """
    Optimize the SQLite database.
    """

    with get_connection() as connection:

        connection.execute("VACUUM")

    logger.info("Database optimized.")