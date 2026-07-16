import os
import subprocess
from unittest.mock import MagicMock, patch

import psutil

from gui.process_action_service import ProcessActionService


def test_kill_process_not_found():

    service = ProcessActionService()

    with patch(
        "psutil.Process",
        side_effect=psutil.NoSuchProcess(1),
    ):

        success, message = service.kill(1)

    assert success is False
    assert message == "Process no longer exists."

def test_kill_access_denied():

    service = ProcessActionService()

    with patch(
        "psutil.Process",
        side_effect=psutil.AccessDenied(1),
    ):

        success, message = service.kill(1)

    assert success is False

    assert "Access denied" in message

def test_kill_protected_process():

    service = ProcessActionService()

    process = MagicMock()

    process.parent.return_value = None

    process.name.return_value = "System"

    with patch(
        "psutil.Process",
        return_value=process,
    ):

        success, message = service.kill(1)

    assert success is False

    assert "protected" in message.lower()

def test_kill_success():

    service = ProcessActionService()

    root = MagicMock()

    root.parent.return_value = None

    root.name.return_value = "chrome.exe"

    root.children.return_value = []

    with patch(
        "psutil.Process",
        return_value=root,
    ):

        with patch(
            "psutil.wait_procs",
            return_value=([], []),
        ):

            success, message = service.kill(1)

    assert success is True

    assert "terminated successfully" in message

    root.kill.assert_called_once()

def test_kill_alive_processes():

    service = ProcessActionService()

    root = MagicMock()

    root.parent.return_value = None

    root.name.return_value = "chrome.exe"

    root.children.return_value = []

    alive = [MagicMock()]

    with patch(
        "psutil.Process",
        return_value=root,
    ):

        with patch(
            "psutil.wait_procs",
            return_value=([], alive),
        ):

            success, message = service.kill(1)

    assert success is False

    assert "Unable to terminate" in message

def test_kill_unexpected_exception():

    service = ProcessActionService()

    process = MagicMock()

    process.parent.side_effect = RuntimeError("Boom")

    with patch(
        "psutil.Process",
        return_value=process,
    ):

        success, message = service.kill(1)

    assert success is False

    assert message == "Boom"

def test_open_location():

    service = ProcessActionService()

    with patch.object(subprocess, "Popen") as popen:

        service.open_location(r"C:\Temp\a.exe")

    popen.assert_called_once_with(
        [
            "explorer",
            "/select,",
            r"C:\Temp\a.exe",
        ]
    )

def test_open_location_empty():

    service = ProcessActionService()

    with patch.object(subprocess, "Popen") as popen:

        service.open_location("")

    popen.assert_not_called()

def test_properties():

    service = ProcessActionService()

    with patch.object(os, "startfile", create=True) as startfile:

        service.properties(r"C:\Temp\a.exe")

    startfile.assert_called_once_with(
        r"C:\Temp\a.exe"
    )

def test_properties_empty():

    service = ProcessActionService()

    with patch.object(os, "startfile", create=True) as startfile:

        service.properties("")

    startfile.assert_not_called()