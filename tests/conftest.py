from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_database():
    """
    Creates a temporary SQLite database for tests.
    """

    with tempfile.TemporaryDirectory() as tmp:

        db_path = Path(tmp) / "history.db"

        connection = sqlite3.connect(db_path)

        yield connection

        connection.close()


@pytest.fixture
def sample_connection():

    from models.connection import ConnectionInfo

    return ConnectionInfo(
        time="12:00:00",
        pid=1234,
        process="chrome.exe",
        protocol="TCP",
        local_ip="192.168.1.5",
        local_port=52000,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="dns.google",
        status="ESTABLISHED",
        path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        publisher="Google LLC",
        country_code="US",
        country_name="United States",
    )


@pytest.fixture
def sample_connections(sample_connection):

    return [
        sample_connection,
        sample_connection,
        sample_connection,
    ]