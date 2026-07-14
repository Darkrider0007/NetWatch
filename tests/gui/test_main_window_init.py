from unittest.mock import MagicMock

import pytest

from gui.main_window import MainWindow


@pytest.fixture
def window(monkeypatch):
    # Prevent background threads
    monkeypatch.setattr(
        "gui.main_window.ConnectionMonitor",
        MagicMock,
    )

    monkeypatch.setattr(
        "gui.main_window.DNSWorker",
        MagicMock,
    )

    monitor = MagicMock()
    monitor.start = MagicMock()

    monkeypatch.setattr(
        "gui.main_window.ConnectionMonitor",
        lambda interval=1: monitor,
    )

    dns = MagicMock()

    monkeypatch.setattr(
        "gui.main_window.DNSWorker",
        lambda: dns,
    )

    return MainWindow()


def test_window_created(window):
    assert window is not None
    assert window.table is not None
    assert window.details is not None
    assert window.filter_bar is not None
    assert window.status is not None


def test_monitor_started(window):
    window.monitor.start.assert_called_once()


def test_saved_settings_loaded(window):
    assert window.filter_state.protocol == "ALL"


def test_connection_selected(window):
    conn = MagicMock()

    window.connection_selected(conn)

    assert window.selected_connection is conn
