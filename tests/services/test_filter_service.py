from services.filter_service import FilterService
from models.connection import ConnectionInfo
from models.filter_state import FilterState


def make_connection():
    return ConnectionInfo(
        time="12:00",
        pid=1,
        process="chrome.exe",
        protocol="TCP",
        local_ip="127.0.0.1",
        local_port=1234,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="google.com",
        status="ESTABLISHED",
        path="",
        publisher="Google",
        country_code="US",
        country_name="United States",
    )


def test_search_filter():
    service = FilterService()

    state = FilterState(search="chrome")

    result = service.filter_connections(
        [make_connection()],
        state,
    )

    assert len(result) == 1


def test_protocol_filter():
    service = FilterService()

    state = FilterState(protocol="UDP")

    result = service.filter_connections(
        [make_connection()],
        state,
    )

    assert result == []


def test_country_filter():
    service = FilterService()

    state = FilterState(country="United States")

    result = service.filter_connections(
        [make_connection()],
        state,
    )

    assert len(result) == 1