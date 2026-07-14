from queue import Empty
from unittest.mock import MagicMock

import pytest

import services.dns_worker as dns_worker
from services.dns_worker import DNSWorker


@pytest.fixture(autouse=True)
def no_background_thread(monkeypatch):
    """Prevent the worker thread from starting."""
    fake_thread = MagicMock()
    monkeypatch.setattr(
        dns_worker,
        "Thread",
        lambda *args, **kwargs: fake_thread,
    )


def test_resolve_empty_ip():
    worker = DNSWorker()

    worker.queue = MagicMock()

    worker.resolve("")

    worker.queue.put.assert_not_called()


def test_resolve_cached_ip():
    worker = DNSWorker()

    worker.cache["8.8.8.8"] = "dns.google"

    received = []

    worker.resolved.connect(
        lambda ip, host: received.append((ip, host))
    )

    worker.resolve("8.8.8.8")

    assert received == [("8.8.8.8", "dns.google")]


def test_resolve_new_ip():
    worker = DNSWorker()

    worker.queue = MagicMock()

    worker.resolve("1.1.1.1")

    worker.queue.put.assert_called_once_with("1.1.1.1")


def test_run_success(monkeypatch):
    worker = DNSWorker()

    worker.queue.get = MagicMock(
        side_effect=[
            "8.8.8.8",
            KeyboardInterrupt,
        ]
    )

    monkeypatch.setattr(
        dns_worker.socket,
        "gethostbyaddr",
        lambda ip: ("dns.google", [], []),
    )

    received = []

    worker.resolved.connect(
        lambda ip, host: received.append((ip, host))
    )

    with pytest.raises(KeyboardInterrupt):
        worker._run()

    assert worker.cache["8.8.8.8"] == "dns.google"
    assert received == [("8.8.8.8", "dns.google")]


def test_run_lookup_failure(monkeypatch):
    worker = DNSWorker()

    worker.queue.get = MagicMock(
        side_effect=[
            "1.1.1.1",
            KeyboardInterrupt,
        ]
    )

    def fail(_):
        raise OSError

    monkeypatch.setattr(
        dns_worker.socket,
        "gethostbyaddr",
        fail,
    )

    received = []

    worker.resolved.connect(
        lambda ip, host: received.append((ip, host))
    )

    with pytest.raises(KeyboardInterrupt):
        worker._run()

    assert worker.cache["1.1.1.1"] == "1.1.1.1"
    assert received == [("1.1.1.1", "1.1.1.1")]


def test_run_queue_empty():
    worker = DNSWorker()

    worker.queue.get = MagicMock(
        side_effect=[
            Empty,
            KeyboardInterrupt,
        ]
    )

    with pytest.raises(KeyboardInterrupt):
        worker._run()