import pytest
from unittest.mock import Mock

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from gui.process_table import ProcessTable
from models.connection import ConnectionInfo


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


@pytest.fixture
def table(mocker):
    mocker.patch(
        "gui.process_table.IconService.get_icon",
        return_value=QIcon(),
    )

    return ProcessTable()


@pytest.fixture
def connection():

    return ConnectionInfo(
        time="12:00:00",
        pid=1234,
        process="chrome.exe",
        protocol="TCP",
        local_ip="192.168.1.5",
        local_port=50000,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="dns.google",
        status="ESTABLISHED",
        path=r"C:\Chrome\chrome.exe",
        publisher="Google LLC",
        country_code="US",
        country_name="United States",
    )


def test_creation(table):

    assert table.rowCount() == 0
    assert table.columnCount() == len(table.HEADERS)


def test_headers(table):

    headers = [
        table.horizontalHeaderItem(i).text()
        for i in range(table.columnCount())
    ]

    assert headers == table.HEADERS


def test_make_key(table, connection):

    key = table.make_key(
        connection.pid,
        connection.local_ip,
        connection.remote_ip,
        connection.remote_port,
        connection.protocol,
    )

    assert key == (
        1234,
        "192.168.1.5",
        "8.8.8.8",
        443,
        "TCP",
    )


def test_add_connection(table, connection):

    table.add_connection(connection)

    assert table.rowCount() == 1


def test_add_multiple_connections(table, connection):

    table.add_connection(connection)

    second = ConnectionInfo(
        time="12:01:00",
        pid=999,
        process="firefox.exe",
        protocol="TCP",
        local_ip="192.168.1.5",
        local_port=50001,
        remote_ip="1.1.1.1",
        remote_port=443,
        remote_host="cloudflare.com",
        status="ESTABLISHED",
        path=r"C:\Firefox\firefox.exe",
        publisher="Mozilla",
        country_code="AU",
        country_name="Australia",
    )

    table.add_connection(second)

    assert table.rowCount() == 2


def test_clear_connections(table, connection):

    table.add_connection(connection)

    table.clear_connections()

    assert table.rowCount() == 0
    assert len(table.connection_rows) == 0


def test_update_hostname(table, connection):

    table.add_connection(connection)

    table.update_hostname(
        "dns.google",
        "google.com",
    )

    assert table.item(
        0,
        table.COL_REMOTE,
    ).text() == "google.com"


def test_update_hostname_unknown_ip(table, connection):

    table.add_connection(connection)

    before = table.item(
        0,
        table.COL_REMOTE,
    ).text()

    table.update_hostname(
        "9.9.9.9",
        "quad9.net",
    )

    after = table.item(
        0,
        table.COL_REMOTE,
    ).text()

    assert before == after


def test_selection_signal(
    table,
    connection,
    qtbot,
):

    table.add_connection(connection)

    with qtbot.waitSignal(
        table.connection_selected
    ):

        table.selectRow(0)


def test_selected_connection_is_correct(
    table,
    connection,
    qtbot,
):

    table.add_connection(connection)

    blocker = qtbot.waitSignal(
        table.connection_selected
    )

    table.selectRow(0)

    emitted = blocker.args[0]

    assert emitted.process == "chrome.exe"


def test_connection_rows_contains_key(
    table,
    connection,
):

    table.add_connection(connection)

    key = table.make_key(
        connection.pid,
        connection.local_ip,
        connection.remote_ip,
        connection.remote_port,
        connection.protocol,
    )

    assert key in table.connection_rows


def test_process_column_text(
    table,
    connection,
):

    table.add_connection(connection)

    assert table.item(
        0,
        table.COL_PROCESS,
    ).text() == "chrome.exe"


def test_country_column_text(
    table,
    connection,
):

    table.add_connection(connection)

    assert table.item(
        0,
        table.COL_COUNTRY,
    ).text() == "United States"


def test_protocol_column_text(
    table,
    connection,
):

    table.add_connection(connection)

    assert table.item(
        0,
        table.COL_PROTOCOL,
    ).text() == "TCP"


def test_status_column_text(
    table,
    connection,
):

    table.add_connection(connection)

    assert table.item(
        0,
        table.COL_STATUS,
    ).text() == "ESTABLISHED"


def test_pid_column_text(
    table,
    connection,
):

    table.add_connection(connection)

    assert table.item(
        0,
        table.COL_PID,
    ).text() == "1234"


def test_remote_port_column(
    table,
    connection,
):

    table.add_connection(connection)

    assert table.item(
        0,
        table.COL_PORT,
    ).text() == "443"


def test_connection_mapping_size(
    table,
    connection,
):

    table.add_connection(connection)

    assert len(table.connection_rows) == 1