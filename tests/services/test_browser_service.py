from unittest.mock import patch

from services.browser_service import BrowserService


@patch("services.browser_service.webbrowser.open")
def test_virustotal_opens_sha256_page(mock_open):

    sha256 = (
        "A83D8E5F7C4B2A1D"
        "9E8F7A6B5C4D3E2F"
        "1A2B3C4D5E6F7081"
        "9A8B7C6D5E4F3A2B"
    )

    result = BrowserService.virustotal(
        sha256
    )

    assert result is True

    mock_open.assert_called_once_with(
        "https://www.virustotal.com/gui/file/"
        + sha256.lower()
    )


@patch("services.browser_service.webbrowser.open")
def test_virustotal_returns_false_for_empty_hash(
    mock_open,
):

    result = BrowserService.virustotal("")

    assert result is False

    mock_open.assert_not_called()


@patch("services.browser_service.webbrowser.open")
def test_virustotal_returns_false_for_whitespace_hash(
    mock_open,
):

    result = BrowserService.virustotal(
        "   "
    )

    assert result is False

    mock_open.assert_not_called()


@patch("services.browser_service.webbrowser.open")
def test_whois_opens_ip_lookup(mock_open):

    result = BrowserService.whois(
        "8.8.8.8"
    )

    assert result is True

    mock_open.assert_called_once_with(
        "https://www.abuseipdb.com/check/8.8.8.8"
    )


@patch("services.browser_service.webbrowser.open")
def test_whois_returns_false_for_empty_ip(
    mock_open,
):

    result = BrowserService.whois("")

    assert result is False

    mock_open.assert_not_called()