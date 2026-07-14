from unittest.mock import patch

from services.browser_service import BrowserService


@patch("webbrowser.open")
def test_open_virustotal(mock_open):
    BrowserService.virustotal("C:/test.exe")
    mock_open.assert_called_once()


@patch("webbrowser.open")
def test_open_whois(mock_open):
    BrowserService.whois("8.8.8.8")
    mock_open.assert_called_once()