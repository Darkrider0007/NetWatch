from unittest.mock import MagicMock

from services.history_search import HistorySearch


def test_search(monkeypatch):

    rows = [
        (1, "chrome.exe"),
        (2, "python.exe"),
    ]

    cursor = MagicMock()
    cursor.fetchall.return_value = rows

    connection = MagicMock()
    connection.cursor.return_value = cursor

    monkeypatch.setattr(
        "services.history_search.get_connection",
        lambda: connection,
    )

    service = HistorySearch()

    result = service.search("chrome")

    cursor.execute.assert_called_once()

    query, params = cursor.execute.call_args.args

    assert "SELECT *" in query
    assert "WHERE process LIKE ?" in query
    assert params == (
        "%chrome%",
        "%chrome%",
        "%chrome%",
        "%chrome%",
    )

    connection.close.assert_called_once()

    assert result == rows


def test_search_empty_text(monkeypatch):

    cursor = MagicMock()
    cursor.fetchall.return_value = []

    connection = MagicMock()
    connection.cursor.return_value = cursor

    monkeypatch.setattr(
        "services.history_search.get_connection",
        lambda: connection,
    )

    service = HistorySearch()

    result = service.search("")

    query, params = cursor.execute.call_args.args

    assert params == (
        "%%",
        "%%",
        "%%",
        "%%",
    )

    connection.close.assert_called_once()

    assert result == []