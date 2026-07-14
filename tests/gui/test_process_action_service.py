import os
import subprocess
from unittest.mock import MagicMock

import psutil

from services.process_action_service import ProcessActionService


def test_kill_success(monkeypatch):
    process = MagicMock()

    monkeypatch.setattr(psutil, "Process", lambda pid: process)

    service = ProcessActionService()

    service.kill(1234)

    process.terminate.assert_called_once()


def test_kill_exception(monkeypatch):
    monkeypatch.setattr(
        psutil,
        "Process",
        MagicMock(side_effect=Exception()),
    )

    service = ProcessActionService()

    service.kill(1234)


def test_open_location(monkeypatch):
    popen = MagicMock()

    monkeypatch.setattr(subprocess, "Popen", popen)

    service = ProcessActionService()

    service.open_location(r"C:\temp\file.txt")

    popen.assert_called_once_with(
        [
            "explorer",
            "/select,",
            r"C:\temp\file.txt",
        ]
    )


def test_open_location_empty(monkeypatch):
    popen = MagicMock()

    monkeypatch.setattr(subprocess, "Popen", popen)

    service = ProcessActionService()

    service.open_location("")

    popen.assert_not_called()


def test_properties(monkeypatch):
    startfile = MagicMock()

    monkeypatch.setattr(os, "startfile", startfile, raising=False)

    service = ProcessActionService()

    service.properties(r"C:\temp\file.txt")

    startfile.assert_called_once_with(r"C:\temp\file.txt")


def test_properties_empty(monkeypatch):
    startfile = MagicMock()

    monkeypatch.setattr(os, "startfile", startfile, raising=False)

    service = ProcessActionService()

    service.properties("")

    startfile.assert_not_called()