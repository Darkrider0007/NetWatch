from unittest.mock import MagicMock, patch

from services.process_service import ProcessService


@patch("services.process_service.psutil.Process")
def test_get_name(mock_process):

    proc = MagicMock()

    proc.name.return_value = "python.exe"
    proc.exe.return_value = "python.exe"
    proc.ppid.return_value = 0
    proc.username.return_value = "user"

    mock_process.return_value = proc

    assert ProcessService.get_name(1) == "python.exe"


@patch("services.process_service.psutil.Process")
def test_get_executable(mock_process):

    proc = MagicMock()

    proc.name.return_value = "python.exe"
    proc.exe.return_value = "C:/python.exe"
    proc.ppid.return_value = 0
    proc.username.return_value = "user"

    mock_process.return_value = proc

    assert ProcessService.get_executable(1) == "C:/python.exe"