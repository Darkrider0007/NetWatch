from types import SimpleNamespace
from typing import Optional
from unittest.mock import MagicMock

import psutil
import pytest

import monitor.network_scanner as scanner_module
from monitor.network_scanner import NetworkScanner


def make_conn(
    *,
    pid: Optional[int] = 100,
    process="python.exe",
    laddr=("192.168.1.10", 5000),
    raddr=("8.8.8.8", 443),
    status="ESTABLISHED",
    type_=1,
):
    conn = SimpleNamespace()

    conn.pid = pid

    conn.laddr = (
        SimpleNamespace(ip=laddr[0], port=laddr[1])
        if laddr
        else ()
    )

    conn.raddr = (
        SimpleNamespace(ip=raddr[0], port=raddr[1])
        if raddr
        else ()
    )

    conn.status = status
    conn.type = type_

    return conn


@pytest.fixture
def scanner():

    process = MagicMock()
    process.get_name.return_value = "python.exe"
    process.get_executable.return_value = r"C:\python.exe"

    dns = MagicMock()
    dns.get.return_value = "dns.google"

    geo = MagicMock()
    geo.country.return_value = ("US", "United States")

    publisher = MagicMock()
    publisher.get_publisher.return_value = "Python"

    settings = SimpleNamespace(resolve_dns=True)

    return NetworkScanner(
        process_service=process,
        dns_service=dns,
        geoip_service=geo,
        publisher_service=publisher,
        settings=settings,
    )


def test_init(scanner):
    assert scanner.last_scan() == []


def test_last_scan(scanner):
    scanner._last_scan = [1, 2]
    assert scanner.last_scan() == [1, 2]


def test_scan_success(monkeypatch, scanner):
    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [make_conn()],
    )

    result = scanner.scan()

    assert len(result) == 1

    item = result[0]

    assert item.pid == 100
    assert item.process == "python.exe"
    assert item.remote_host == "dns.google"
    assert item.publisher == "Python"
    assert item.country_name == "United States"


def test_scan_udp(monkeypatch, scanner):
    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [
            make_conn(type_=2),
        ],
    )

    result = scanner.scan()

    assert result[0].protocol == "UDP"


def test_dns_disabled(monkeypatch, scanner):
    scanner.settings.resolve_dns = False

    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [make_conn()],
    )

    result = scanner.scan()

    assert result[0].remote_host == "8.8.8.8"


def test_skip_pid_none(monkeypatch, scanner):
    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [
            make_conn(pid=None),
        ],
    )

    assert scanner.scan() == []


def test_skip_system_process(monkeypatch, scanner):
    scanner.process_service.get_name.return_value = "System"

    monkeypatch.setattr(
        scanner_module,
        "is_system_process",
        lambda _: True,
    )

    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [make_conn()],
    )

    assert scanner.scan() == []


def test_skip_loopback(monkeypatch, scanner):
    monkeypatch.setattr(
        scanner_module,
        "is_loopback",
        lambda _: True,
    )

    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [make_conn()],
    )

    assert scanner.scan() == []


def test_net_connections_exception(monkeypatch, scanner):
    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        MagicMock(side_effect=RuntimeError("boom")),
    )

    assert scanner.scan() == []


@pytest.mark.parametrize(
    "exc",
    [
        psutil.NoSuchProcess(1),
        psutil.AccessDenied(1),
        AttributeError(),
    ],
)
def test_ignored_process_exceptions(monkeypatch, scanner, exc):
    scanner.process_service.get_name.side_effect = exc

    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [make_conn()],
    )

    assert scanner.scan() == []


def test_generic_exception(monkeypatch, scanner):
    scanner.geoip_service.country.side_effect = RuntimeError("geo")

    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [make_conn()],
    )

    assert scanner.scan() == []


def test_empty_addresses(monkeypatch, scanner):
    monkeypatch.setattr(
        scanner_module.psutil,
        "net_connections",
        lambda kind="inet": [
            make_conn(laddr=None, raddr=None),
        ],
    )

    result = scanner.scan()

    assert len(result) == 0