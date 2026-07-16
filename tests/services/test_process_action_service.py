import os
import subprocess
from unittest.mock import patch

import psutil

from services.process_action_service import ProcessActionService


def test_kill_process():
    service = ProcessActionService()

    process = patch("psutil.Process").start()

    service.kill(123)

    process.assert_called_once_with(123)
    process.return_value.terminate.assert_called_once()

    patch.stopall()


def test_kill_exception():
    service = ProcessActionService()

    with patch(
        "psutil.Process",
        side_effect=Exception("Boom"),
    ):
        # Should not raise
        service.kill(123)


def test_open_location():
    service = ProcessActionService()

    with patch.object(subprocess, "Popen") as popen:

        service.open_location(r"C:\Temp\test.exe")

    popen.assert_called_once_with(
        [
            "explorer",
            "/select,",
            r"C:\Temp\test.exe",
        ]
    )


def test_open_location_empty():
    service = ProcessActionService()

    with patch.object(subprocess, "Popen") as popen:

        service.open_location("")

    popen.assert_not_called()


def test_properties():
    service = ProcessActionService()

    with patch.object(
        os,
        "startfile",
        create=True,
    ) as startfile:

        service.properties(r"C:\Temp\test.exe")

    startfile.assert_called_once_with(
        r"C:\Temp\test.exe"
    )


def test_properties_empty():
    service = ProcessActionService()

    with patch.object(
        os,
        "startfile",
        create=True,
    ) as startfile:

        service.properties("")

    startfile.assert_not_called()