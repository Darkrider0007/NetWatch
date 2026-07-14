from monitor.connection_cache import ConnectionCache
from models.connection import ConnectionInfo


def make_connection(
    pid=1,
    remote_ip="8.8.8.8",
    remote_port=443,
):
    return ConnectionInfo(
        time="12:00",
        pid=pid,
        process="chrome.exe",
        protocol="TCP",
        local_ip="127.0.0.1",
        local_port=50000,
        remote_ip=remote_ip,
        remote_port=remote_port,
        remote_host="google.com",
        status="ESTABLISHED",
        path="C:/chrome.exe",
    )


def test_make_key():
    cache = ConnectionCache()
    conn = make_connection()

    key = cache.make_key(conn)

    assert key == (
        conn.pid,
        conn.local_ip,
        conn.local_port,
        conn.remote_ip,
        conn.remote_port,
        conn.protocol,
    )


def test_compare_first_scan():
    cache = ConnectionCache()

    conn = make_connection()

    result = cache.compare([conn])

    assert len(result["added"]) == 1
    assert len(result["removed"]) == 0
    assert len(result["updated"]) == 0
    assert len(result["current"]) == 1


def test_compare_same_connections():
    cache = ConnectionCache()

    conn = make_connection()

    cache.compare([conn])

    result = cache.compare([conn])

    assert result["added"] == []
    assert result["removed"] == []
    assert result["updated"] == []


def test_compare_removed_connection():
    cache = ConnectionCache()

    conn = make_connection()

    cache.compare([conn])

    result = cache.compare([])

    assert len(result["removed"]) == 1
    assert result["added"] == []
    assert result["updated"] == []


def test_compare_added_connection():
    cache = ConnectionCache()

    conn1 = make_connection()
    conn2 = make_connection(
        pid=2,
        remote_ip="1.1.1.1",
    )

    cache.compare([conn1])

    result = cache.compare([conn1, conn2])

    assert len(result["added"]) == 1
    assert result["added"][0].pid == 2


def test_compare_updated_connection():
    cache = ConnectionCache()

    old = make_connection()

    new = make_connection()
    new.remote_host = "dns.google"

    cache.compare([old])

    result = cache.compare([new])

    assert len(result["updated"]) == 1
    assert result["updated"][0].remote_host == "dns.google"