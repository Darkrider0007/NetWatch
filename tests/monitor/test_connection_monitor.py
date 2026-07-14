from unittest.mock import MagicMock

import pytest

import monitor.connection_monitor as monitor_module
from monitor.connection_monitor import ConnectionMonitor


@pytest.fixture
def monitor(monkeypatch):
    scanner = MagicMock()
    cache = MagicMock()

    monkeypatch.setattr(
        monitor_module,
        "NetworkScanner",
        lambda: scanner,
    )

    monkeypatch.setattr(
        monitor_module,
        "ConnectionCache",
        lambda: cache,
    )

    m = ConnectionMonitor(interval=0.1)

    return m, scanner, cache


def test_init(monitor):
    m, scanner, cache = monitor

    assert m.interval == 0.1
    assert m.scanner is scanner
    assert m.cache is cache
    assert m._running is True


def test_stop(monitor):
    m, _, _ = monitor

    m._running = True

    m.stop()

    assert m._running is False


def test_run_success(monkeypatch, monitor):
    m, scanner, cache = monitor

    scanner.scan.return_value = ["conn1"]

    cache.compare.return_value = {
        "current": ["conn1"]
    }

    received = []

    m.connections_updated.connect(
        lambda changes: received.append(changes)
    )

    def fake_sleep(_):
        m._running = False

    monkeypatch.setattr(
        m,
        "msleep",
        fake_sleep,
    )

    m.run()

    scanner.scan.assert_called_once()

    cache.compare.assert_called_once_with(
        ["conn1"]
    )

    assert received == [
        {"current": ["conn1"]}
    ]


def test_run_exception(monkeypatch, monitor):
    m, scanner, _ = monitor

    scanner.scan.side_effect = RuntimeError(
        "boom"
    )

    errors = []

    m.monitor_error.connect(
        lambda message: errors.append(message)
    )

    def fake_sleep(_):
        m._running = False

    monkeypatch.setattr(
        m,
        "msleep",
        fake_sleep,
    )

    m.run()

    assert errors == ["boom"]