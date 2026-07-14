import sqlite3

from database.database import (
    initialize_database,
    get_connection,
    clear_history,
    get_history,
    get_total_records,
)


def test_database_initialization():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='connections'
        """
    )

    table = cursor.fetchone()

    connection.close()

    assert table is not None


def test_history_initially_returns_list():

    initialize_database()

    history = get_history()

    assert isinstance(history, list)


def test_clear_history():

    initialize_database()

    clear_history()

    assert get_total_records() == 0


def test_total_records_returns_integer():

    initialize_database()

    total = get_total_records()

    assert isinstance(total, int)


def test_connection_returns_sqlite_connection():

    connection = get_connection()

    assert isinstance(connection, sqlite3.Connection)

    connection.close()


def test_connections_table_columns():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        PRAGMA table_info(connections)
        """
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    connection.close()

    expected = [
        "id",
        "time",
        "process",
        "publisher",
        "pid",
        "protocol",
        "local_ip",
        "local_port",
        "remote_ip",
        "remote_port",
        "remote_host",
        "country",
        "status",
        "bytes_sent",
        "bytes_received",
    ]

    for column in expected:

        assert column in columns