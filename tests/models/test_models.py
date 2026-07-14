from models.connection import ConnectionInfo
from models.settings import Settings


def test_connection_info_creation():

    connection = ConnectionInfo(
        time="12:00:00",
        pid=1234,
        process="chrome.exe",
        protocol="TCP",
        local_ip="192.168.1.10",
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

    assert connection.time == "12:00:00"
    assert connection.pid == 1234
    assert connection.process == "chrome.exe"
    assert connection.protocol == "TCP"
    assert connection.remote_ip == "8.8.8.8"
    assert connection.remote_port == 443
    assert connection.publisher == "Google LLC"
    assert connection.country_name == "United States"


def test_connection_default_values():

    connection = ConnectionInfo(
        time="00:00:00",
        pid=1,
        process="python.exe",
        protocol="UDP",
        local_ip="127.0.0.1",
        local_port=8000,
        remote_ip="",
        remote_port=0,
        remote_host="",
        status="LISTEN",
        path="python.exe",
    )

    assert connection.bytes_sent == 0
    assert connection.bytes_received == 0
    assert connection.packets_sent == 0
    assert connection.packets_received == 0
    assert connection.publisher == ""
    assert connection.country_code == ""
    assert connection.country_name == ""


def test_connection_getitem():

    connection = ConnectionInfo(
        time="10:10:10",
        pid=55,
        process="test.exe",
        protocol="TCP",
        local_ip="1.1.1.1",
        local_port=1000,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="dns.google",
        status="ESTABLISHED",
        path="test.exe",
    )

    assert connection["pid"] == 55
    assert connection["process"] == "test.exe"
    assert connection["remote_ip"] == "8.8.8.8"


def test_settings_defaults():

    settings = Settings()

    assert settings.refresh_interval == 1000
    assert settings.resolve_dns is False
    assert settings.show_system_processes is False
    assert settings.show_private_network is False
    assert settings.auto_scroll is True


def test_settings_can_be_modified():

    settings = Settings()

    settings.refresh_interval = 500
    settings.resolve_dns = True
    settings.auto_scroll = False

    assert settings.refresh_interval == 500
    assert settings.resolve_dns is True
    assert settings.auto_scroll is False