from unittest.mock import MagicMock, patch

from models.connection import ConnectionInfo
from services.history_service import HistoryService


def make_connection():

    return ConnectionInfo(
        time="12:00",
        pid=1,
        process="chrome.exe",
        protocol="TCP",
        local_ip="127.0.0.1",
        local_port=1111,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="google.com",
        status="ESTABLISHED",
        path="",
        publisher="Google",
        country_code="US",
        country_name="United States",
    )


@patch("services.history_service.get_connection")
def test_save(mock_conn):

    conn = MagicMock()

    mock_conn.return_value = conn

    HistoryService().save([make_connection()])

    conn.cursor.return_value.execute.assert_called()
    conn.commit.assert_called_once()


@patch("services.history_service.get_connection")
def test_clear(mock_conn):

    conn = MagicMock()

    mock_conn.return_value = conn

    HistoryService().clear()

    conn.execute.assert_called_once()
    conn.commit.assert_called_once()