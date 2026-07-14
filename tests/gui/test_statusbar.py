import pytest
from PySide6.QtWidgets import QApplication

from gui.statusbar import MainStatusBar


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


def test_statusbar_creation(app):
    status = MainStatusBar()

    assert status.connection_label.text() == "Connections : 0"
    assert status.process_label.text() == "Processes : 0"


def test_update_counts(app):
    status = MainStatusBar()

    status.update_counts(
        connections=15,
        processes=6,
    )

    assert status.connection_label.text() == "Connections : 15"
    assert status.process_label.text() == "Processes : 6"


def test_update_counts_multiple_times(app):
    status = MainStatusBar()

    status.update_counts(5, 2)

    assert status.connection_label.text() == "Connections : 5"
    assert status.process_label.text() == "Processes : 2"

    status.update_counts(20, 8)

    assert status.connection_label.text() == "Connections : 20"
    assert status.process_label.text() == "Processes : 8"


def test_zero_counts(app):
    status = MainStatusBar()

    status.update_counts(0, 0)

    assert status.connection_label.text() == "Connections : 0"
    assert status.process_label.text() == "Processes : 0"


def test_large_counts(app):
    status = MainStatusBar()

    status.update_counts(
        99999,
        12345,
    )

    assert status.connection_label.text() == "Connections : 99999"
    assert status.process_label.text() == "Processes : 12345"