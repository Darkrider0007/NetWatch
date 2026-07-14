import pytest
from PySide6.QtWidgets import QApplication

from gui.filter_bar import FilterBar


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_filter_bar_creation(app):
    bar = FilterBar()

    assert bar.search is not None
    assert bar.protocol is not None
    assert bar.country is not None
    assert bar.publisher is not None
    assert bar.established is not None
    assert bar.system is not None


def test_default_protocol(app):
    bar = FilterBar()

    assert bar.protocol.currentText() == "ALL"


def test_default_country(app):
    bar = FilterBar()

    assert bar.country.currentText() == "ALL"


def test_default_publisher(app):
    bar = FilterBar()

    assert bar.publisher.currentText() == "ALL"


def test_search_text(app):
    bar = FilterBar()

    bar.search.setText("chrome")

    assert bar.search.text() == "chrome"


def test_protocol_change(app):
    bar = FilterBar()

    bar.protocol.setCurrentText("TCP")

    assert bar.protocol.currentText() == "TCP"


def test_country_population(app):
    bar = FilterBar()

    countries = [
        "India",
        "United States",
        "Japan",
    ]

    bar.set_countries(countries)

    assert bar.country.count() == 4
    assert bar.country.itemText(0) == "ALL"


def test_publisher_population(app):
    bar = FilterBar()

    publishers = [
        "Google",
        "Microsoft",
    ]

    bar.set_publishers(publishers)

    assert bar.publisher.count() == 3
    assert bar.publisher.itemText(0) == "ALL"


def test_established_checkbox(app):
    bar = FilterBar()

    bar.established.setChecked(True)

    assert bar.established.isChecked()


def test_system_checkbox(app):
    bar = FilterBar()

    bar.system.setChecked(True)

    assert bar.system.isChecked()


def test_search_signal(app, qtbot):
    bar = FilterBar()

    with qtbot.waitSignal(bar.search_changed):
        bar.search.setText("edge")


def test_protocol_signal(app, qtbot):
    bar = FilterBar()

    with qtbot.waitSignal(bar.protocol_changed):
        bar.protocol.setCurrentText("UDP")


def test_country_signal(app, qtbot):
    bar = FilterBar()

    bar.set_countries(["India"])

    with qtbot.waitSignal(bar.country_changed):
        bar.country.setCurrentText("India")


def test_publisher_signal(app, qtbot):
    bar = FilterBar()

    bar.set_publishers(["Google"])

    with qtbot.waitSignal(bar.publisher_changed):
        bar.publisher.setCurrentText("Google")


def test_established_signal(app, qtbot):
    bar = FilterBar()

    with qtbot.waitSignal(bar.established_changed):
        bar.established.setChecked(True)


def test_system_signal(app, qtbot):
    bar = FilterBar()

    with qtbot.waitSignal(bar.system_changed):
        bar.system.setChecked(True)