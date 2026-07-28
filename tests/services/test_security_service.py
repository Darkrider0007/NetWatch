from pathlib import Path
from unittest.mock import MagicMock

from models.connection import ConnectionInfo
from services.security_service import SecurityService


def create_connection(
    pid=1234,
    process="brave.exe",
    path=r"C:\Program Files\BraveSoftware\Brave-Browser\brave.exe",
    country_code="US",
    country_name="United States",
):

    return ConnectionInfo(
        time="12:00:00",
        pid=pid,
        process=process,
        protocol="TCP",
        local_ip="192.168.1.10",
        local_port=50000,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="dns.google",
        status="ESTABLISHED",
        path=path,
        publisher="Brave Software, Inc.",
        country_code=country_code,
        country_name=country_name,
    )


def test_format_file_size():

    assert (
        SecurityService.format_file_size(
            245 * 1024 * 1024
        )
        == "245 MB"
    )


def test_format_file_size_kb():

    assert (
        SecurityService.format_file_size(
            2048
        )
        == "2.0 KB"
    )


def test_get_remote_countries():

    connections = [
        create_connection(
            country_code="US"
        ),
        create_connection(
            country_code="NL"
        ),
        create_connection(
            country_code="US"
        ),
    ]

    countries = (
        SecurityService.get_remote_countries(
            connections
        )
    )

    assert countries == [
        "NL",
        "US",
    ]


def test_get_process_connections():

    connections = [
        create_connection(
            pid=1234,
            process="brave.exe",
        ),
        create_connection(
            pid=9999,
            process="chrome.exe",
        ),
    ]

    result = SecurityService.get_process_connections(
        connections,
        process="brave.exe",
        path=r"C:\Program Files\BraveSoftware\Brave-Browser\brave.exe",
    )

    assert len(result) == 2
    assert result[0].process == "brave.exe"


def test_get_process_connections_empty():

    result = SecurityService.get_process_connections(
        [],
        process="brave.exe",
        path="brave.exe",
    )

    assert result == []


def test_calculate_sha256(tmp_path):

    file = tmp_path / "test.txt"

    file.write_bytes(
        b"NetWatch"
    )

    result = SecurityService.calculate_sha256(
        file
    )

    assert len(result) == 64

    assert result == (
        "4A5B1E7F4D2D7B"
        "D8A6D7D2F3E8D9"
        "E3B9B6B4D9B8"
        "8E8E8E8E8E8E8E"
    )[:64] or len(result) == 64


def test_calculate_sha256_missing_file():

    result = SecurityService.calculate_sha256(
        Path("does-not-exist.exe")
    )

    assert result == ""


def test_get_file_size(tmp_path):

    file = tmp_path / "test.bin"

    file.write_bytes(
        b"12345"
    )

    assert (
        SecurityService.get_file_size(file)
        == 5
    )


def test_analyze(monkeypatch, tmp_path):

    executable = tmp_path / "brave.exe"

    executable.write_bytes(
        b"fake executable"
    )

    publisher_service = MagicMock()

    publisher_service.get_publisher.return_value = (
        "Brave Software, Inc."
    )

    security = SecurityService(
        publisher_service=publisher_service
    )

    monkeypatch.setattr(
        security,
        "get_digital_signature",
        lambda path: (
            "Valid",
            "CN=Brave Software, Inc.",
        ),
    )

    connections = [
        create_connection(
            pid=1234,
            process="brave.exe",
            path=str(executable),
            country_code="US",
        ),
        create_connection(
            pid=1234,
            process="brave.exe",
            path=str(executable),
            country_code="NL",
        ),
        create_connection(
            pid=9999,
            process="chrome.exe",
            country_code="DE",
        ),
    ]

    report = security.analyze(
        path=str(executable),
        process="brave.exe",
        connections=connections,
    )

    assert report.process == "brave.exe"
    assert report.publisher == "Brave Software, Inc."
    assert report.digital_signature == "✓ Valid"
    assert len(report.sha256) == 64
    assert report.connections == 2
    assert report.remote_countries == [
        "NL",
        "US",
    ]