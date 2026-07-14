import pytest
from PySide6.QtWidgets import QApplication

from gui.details_panel import DetailsPanel
from models.connection import ConnectionInfo
from collections import Counter

@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def make_connection():
    return ConnectionInfo(
        time="12:00:00",
        pid=1234,
        process="chrome.exe",
        protocol="TCP",
        local_ip="127.0.0.1",
        local_port=50500,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="dns.google",
        status="ESTABLISHED",
        path="C:/Program Files/Google/Chrome/Application/chrome.exe",
        publisher="Google LLC",
        country_code="US",
        country_name="United States",
    )


def test_creation(app):
    panel = DetailsPanel()

    assert panel.count() == 0


def test_update_connection(app):
    panel = DetailsPanel()

    panel.update_connection(make_connection())

    assert panel.count() == 7

    assert panel.item(0).text() == "Process : chrome.exe"
    assert panel.item(1).text() == "Publisher : Google LLC"
    assert panel.item(2).text() == "PID : 1234"
    assert panel.item(3).text() == "Protocol : TCP"
    assert panel.item(4).text() == "Remote : dns.google"
    assert panel.item(5).text() == "Country : United States"
    assert panel.item(6).text() == "Status : ESTABLISHED"


def test_update_statistics_empty(app):
    panel = DetailsPanel()

    stats = {
        "total": 0,
        "processes": Counter(),
        "countries": Counter(),
    }

    panel.update_statistics(stats)

    assert panel.count() >= 4
    assert panel.item(0).text() == "Connections : 0"


def test_update_statistics(app):
    panel = DetailsPanel()

    stats = {
        "total": 5,
        "processes": Counter({
            "chrome.exe": 3,
            "python.exe": 2,
        }),
        "countries": Counter({
            "India": 4,
            "United States": 1,
        }),
    }

    panel.update_statistics(stats)

    texts = [
        panel.item(i).text()
        for i in range(panel.count())
    ]

    assert "Connections : 5" in texts
    assert "Top Processes" in texts
    assert "Top Countries" in texts
    assert "chrome.exe (3)" in texts
    assert "python.exe (2)" in texts
    assert "United States (1)" in texts
    assert "India (4)" in texts


def test_update_connection_replaces_previous_data(app):
    panel = DetailsPanel()

    panel.update_connection(make_connection())

    conn = make_connection()
    conn.process = "firefox.exe"
    conn.publisher = "Mozilla"

    panel.update_connection(conn)

    assert panel.item(0).text() == "Process : firefox.exe"
    assert panel.item(1).text() == "Publisher : Mozilla"


def test_statistics_replaces_connection_details(app):
    panel = DetailsPanel()

    panel.update_connection(make_connection())

    stats = {
        "total": 2,
        "processes": Counter(),
        "countries": Counter(),
    }

    panel.update_statistics(stats)

    assert panel.item(0).text() == "Connections : 2"