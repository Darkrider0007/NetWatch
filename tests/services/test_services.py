from pathlib import Path
from unittest.mock import MagicMock

import pytest

from models.connection import ConnectionInfo
from models.filter_state import FilterState

from services.dns_service import DNSService
from services.filter_service import FilterService
from services.geoip_service import GeoIPService
from services.history_service import HistoryService
from services.process_service import ProcessService
from services.publisher_service import PublisherService


# ==========================================================
# DNS SERVICE
# ==========================================================

def test_dns_cache_empty():

    dns = DNSService()

    assert dns.get("8.8.8.8") is None


def test_dns_put_and_get():

    dns = DNSService()

    dns.put(
        "8.8.8.8",
        "dns.google",
    )

    assert dns.get("8.8.8.8") == "dns.google"


def test_dns_overwrite():

    dns = DNSService()

    dns.put("1.1.1.1", "one.one.one.one")
    dns.put("1.1.1.1", "cloudflare")

    assert dns.get("1.1.1.1") == "cloudflare"


# ==========================================================
# FILTER SERVICE
# ==========================================================

@pytest.fixture
def sample_connection():

    return ConnectionInfo(
        time="12:00",
        pid=100,
        process="chrome.exe",
        protocol="TCP",
        local_ip="192.168.1.10",
        local_port=50000,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="dns.google",
        status="ESTABLISHED",
        path="chrome.exe",
        publisher="Google",
        country_code="US",
        country_name="United States",
    )


def test_filter_no_filters(sample_connection):

    state = FilterState()

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert len(result) == 1


def test_filter_search(sample_connection):

    state = FilterState()

    state.search = "chrome"

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert len(result) == 1


def test_filter_search_not_found(sample_connection):

    state = FilterState()

    state.search = "firefox"

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert result == []


def test_filter_protocol(sample_connection):

    state = FilterState()

    state.protocol = "UDP"

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert result == []


def test_filter_country(sample_connection):

    state = FilterState()

    state.country = "United States"

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert len(result) == 1


def test_filter_publisher(sample_connection):

    state = FilterState()

    state.publisher = "Google"

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert len(result) == 1


def test_filter_established(sample_connection):

    state = FilterState()

    state.established_only = True

    result = FilterService().filter_connections(
        [sample_connection],
        state,
    )

    assert len(result) == 1


# ==========================================================
# PROCESS SERVICE
# ==========================================================

def test_process_none(mocker):

    mocker.patch(
        "services.process_service.ProcessService.get_process",
        return_value=None,
    )

    assert ProcessService.get_process_info(1) is None


def test_process_name_unknown(mocker):

    mocker.patch(
        "services.process_service.ProcessService.get_process_info",
        return_value=None,
    )

    assert ProcessService.get_name(999) == "Unknown"


def test_process_executable_unknown(mocker):

    mocker.patch(
        "services.process_service.ProcessService.get_process_info",
        return_value=None,
    )

    assert ProcessService.get_executable(999) == ""


# ==========================================================
# PUBLISHER SERVICE
# ==========================================================

def test_empty_executable():

    service = PublisherService()

    assert service.get_publisher("") == ""


def test_missing_file():

    service = PublisherService()

    assert service.get_publisher(
        "C:/does/not/exist.exe"
    ) == ""


def test_invalid_pe_file(tmp_path):

    exe = tmp_path / "dummy.exe"

    exe.write_text("hello")

    service = PublisherService()

    assert service.get_publisher(
        str(exe)
    ) == ""


# ==========================================================
# GEOIP SERVICE
# ==========================================================

def test_geoip_cache(mocker):

    fake_reader = MagicMock()

    fake_response = MagicMock()

    fake_response.country.iso_code = "US"

    fake_response.country.name = "United States"

    fake_reader.country.return_value = fake_response

    mocker.patch(
        "geoip2.database.Reader",
        return_value=fake_reader,
    )

    geo = GeoIPService()

    result1 = geo.country("8.8.8.8")

    result2 = geo.country("8.8.8.8")

    assert result1 == result2

    assert fake_reader.country.call_count == 1


def test_geoip_exception(mocker):

    fake_reader = MagicMock()

    fake_reader.country.side_effect = Exception()

    mocker.patch(
        "geoip2.database.Reader",
        return_value=fake_reader,
    )

    geo = GeoIPService()

    assert geo.country("1.1.1.1") == ("", "")


# ==========================================================
# HISTORY SERVICE
# ==========================================================

def test_history_clear(mocker):

    connection = MagicMock()

    mocker.patch(
        "services.history_service.get_connection",
        return_value=connection,
    )

    HistoryService().clear()

    connection.execute.assert_called_once()

    connection.commit.assert_called_once()

    connection.close.assert_called_once()


def test_history_save(mocker, sample_connection):

    connection = MagicMock()

    mocker.patch(
        "services.history_service.get_connection",
        return_value=connection,
    )

    HistoryService().save(
        [sample_connection]
    )

    assert connection.cursor.return_value.execute.called

    connection.commit.assert_called_once()

    connection.close.assert_called_once()