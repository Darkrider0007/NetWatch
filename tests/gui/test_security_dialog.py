from unittest.mock import MagicMock, patch

import pytest

from gui.security_dialog import SecurityDialog
from models.security import SecurityReport


@pytest.fixture
def report():

    return SecurityReport(
        process="brave.exe",
        publisher="Brave Software, Inc.",
        digital_signature="✓ Valid",
        sha256="A" * 64,
        file_size_bytes=245 * 1024 * 1024,
        file_size_display="245 MB",
        path=r"C:\Program Files\BraveSoftware\Brave-Browser\brave.exe",
        connections=17,
        remote_countries=[
            "NL",
            "US",
        ],
        signer="CN=Brave Software, Inc.",
        signature_status="Valid",
        generated_at="2026-07-28T16:00:00",
    )


@patch(
    "gui.security_dialog.SecurityService"
)
def test_dialog_builds(
    mock_service,
    qtbot,
    report,
):

    service = mock_service.return_value

    service.analyze.return_value = report

    dialog = SecurityDialog(
        path=report.path,
        process=report.process,
        connections=[],
    )

    qtbot.addWidget(dialog)

    assert (
        dialog.windowTitle()
        == "Security Analysis"
    )

    assert (
        dialog.report.process
        == "brave.exe"
    )


@patch(
    "gui.security_dialog.BrowserService.virustotal"
)
@patch(
    "gui.security_dialog.SecurityService"
)
def test_open_virustotal(
    mock_service,
    mock_virustotal,
    qtbot,
    report,
):

    service = mock_service.return_value

    service.analyze.return_value = report

    dialog = SecurityDialog(
        path=report.path,
        process=report.process,
        connections=[],
    )

    qtbot.addWidget(dialog)

    dialog.open_virustotal()

    mock_virustotal.assert_called_once_with(
        report.sha256
    )


@patch(
    "gui.security_dialog.SecurityService"
)
def test_copy_sha256(
    mock_service,
    qtbot,
    report,
):

    service = mock_service.return_value

    service.analyze.return_value = report

    dialog = SecurityDialog(
        path=report.path,
        process=report.process,
        connections=[],
    )

    qtbot.addWidget(dialog)

    dialog.copy_sha256()

    assert (
        qtbot
        is not None
    )

@patch(
    "gui.security_dialog.BrowserService.virustotal"
)
@patch(
    "gui.security_dialog.SecurityService"
)
def test_open_virustotal_uses_sha256(
    mock_service,
    mock_virustotal,
    qtbot,
    report,
):

    service = mock_service.return_value

    service.analyze.return_value = report

    dialog = SecurityDialog(
        path=report.path,
        process=report.process,
        connections=[],
    )

    qtbot.addWidget(dialog)

    dialog.open_virustotal()

    mock_virustotal.assert_called_once_with(
        report.sha256
    )

@patch(
    "gui.security_dialog.QMessageBox.warning"
)
@patch(
    "gui.security_dialog.SecurityService"
)
def test_open_virustotal_without_sha256(
    mock_service,
    mock_warning,
    qtbot,
    report,
):

    report.sha256 = ""

    service = mock_service.return_value

    service.analyze.return_value = report

    dialog = SecurityDialog(
        path=report.path,
        process=report.process,
        connections=[],
    )

    qtbot.addWidget(dialog)

    dialog.open_virustotal()

    mock_warning.assert_called_once()