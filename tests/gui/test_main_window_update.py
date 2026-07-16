from types import SimpleNamespace
from typing import cast
from unittest.mock import MagicMock

from gui.main_window import MainWindow


def create_window():
    window = MainWindow.__new__(MainWindow)

    window.filter_state = MagicMock()

    window.filter_service = MagicMock()
    window.filter_service.filter_connections = MagicMock()

    window.table = MagicMock()
    window.table.clear_connections = MagicMock()
    window.table.add_connection = MagicMock()
    window.table.update_hostname = MagicMock()

    window.status = MagicMock()
    window.status.update_counts = MagicMock()
    window.status.showMessage = MagicMock()

    window.statistics = MagicMock()
    window.statistics.build = MagicMock(return_value={})

    window.details = MagicMock()
    window.details.update_statistics = MagicMock()
    window.details.update_connection = MagicMock()

    window.dns_worker = MagicMock()
    window.dns_worker.resolve = MagicMock()

    window.notification_service = MagicMock()
    window.notification_service.notify = MagicMock()

    window.history_service = MagicMock()
    window.history_service.save = MagicMock()
    window.history_service.clear = MagicMock()

    window.monitor = MagicMock()
    window.monitor.scanner = MagicMock()
    window.monitor.scanner.last_scan = MagicMock(return_value=[])

    window.monitor.scanner.dns_service = MagicMock()
    window.monitor.scanner.dns_service.put = MagicMock()

    window.selected_connection = None
    window.notification_enabled = True
    
    return window


def test_update_connections():
    window = create_window()

    connection = SimpleNamespace(
        pid=10,
        remote_ip="8.8.8.8",
        remote_port=443,
        process="chrome.exe",
        remote_host="dns.google",
    )

    window.filter_service.filter_connections.return_value = [ # type: ignore
        connection
    ]

    window.update_connections(
        {
            "current": [connection],
            "added": [connection],
        }
    )

    window.table.clear_connections.assert_called_once() # type: ignore
    window.table.add_connection.assert_called_once_with(connection) # type: ignore
    window.dns_worker.resolve.assert_called_once_with("8.8.8.8") # type: ignore
    window.status.update_counts.assert_called_once_with(1, 1) # type: ignore
    window.statistics.build.assert_called_once_with([connection]) # type: ignore
    window.details.update_statistics.assert_called_once_with({}) # type: ignore
    window.notification_service.notify.assert_called_once() # type: ignore
    window.history_service.save.assert_called_once_with([connection]) # type: ignore


def test_connection_selected():
    window = create_window()

    connection = object()

    window.connection_selected(connection)

    window.notification_enabled = True

    assert window.selected_connection is connection

    window.details.update_connection.assert_called_once_with( # type: ignore
        connection
    )


def test_update_filter():
    window = create_window()

    window.update_connections = MagicMock()

    window.update_filter("search", "python")

    assert window.filter_state.search == "python"

    window.update_connections.assert_called_once_with(
        {
            "current": [],
        }
    )


def test_hostname_resolved():
    window = create_window()

    window.hostname_resolved(
        "8.8.8.8",
        "dns.google",
    )

    cast(MagicMock, window.monitor.scanner.dns_service.put).assert_called_once_with(
        "8.8.8.8",
        "dns.google",
    )

    window.table.update_hostname.assert_called_once_with( # type: ignore
        "8.8.8.8",
        "dns.google",
    )


def test_show_error():
    window = create_window()

    statusbar = MagicMock()
    statusbar.showMessage = MagicMock()

    window.statusBar = MagicMock(return_value=statusbar)

    window.show_error("Something failed")

    statusbar.showMessage.assert_called_once_with(
        "Something failed",
        5000,
    )


def test_notifications_disabled():

    window = create_window()

    window.notification_enabled = False

    connection = SimpleNamespace(
        pid=10,
        remote_ip="8.8.8.8",
        remote_port=443,
        process="chrome.exe",
        remote_host="dns.google",
    )

    window.filter_service.filter_connections.return_value = [ # type: ignore
        connection
    ]

    window.update_connections(
        {
            "current": [connection],
            "added": [connection],
        }
    )

    window.notification_service.notify.assert_not_called() # type: ignore


def test_no_added_connections():

    window = create_window()

    connection = SimpleNamespace(
        pid=10,
        remote_ip="8.8.8.8",
        remote_port=443,
        process="chrome.exe",
        remote_host="dns.google",
    )

    window.filter_service.filter_connections.return_value = [ # type: ignore
        connection
    ]

    window.update_connections(
        {
            "current": [connection],
            "added": [],
        }
    )

    window.notification_service.notify.assert_not_called() # type: ignore


def test_notification_message():

    window = create_window()

    connection = SimpleNamespace(
        pid=10,
        remote_ip="8.8.8.8",
        remote_port=443,
        process="chrome.exe",
        remote_host="dns.google",
    )

    window.filter_service.filter_connections.return_value = [ # type: ignore
        connection
    ]

    window.update_connections(
        {
            "current": [connection],
            "added": [connection],
        }
    )

    window.notification_service.notify.assert_called_once_with( # type: ignore
        "New Network Activity",
        "chrome.exe\nConnected to dns.google:443",
    )