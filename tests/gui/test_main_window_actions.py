from types import SimpleNamespace
from unittest.mock import MagicMock

from gui.main_window import MainWindow


def create_window():
    window = MainWindow.__new__(MainWindow)

    window.monitor = MagicMock()
    window.monitor.start = MagicMock()
    window.monitor.stop = MagicMock()
    window.monitor.wait = MagicMock()
    window.monitor.isRunning = MagicMock(return_value=False)

    window.process_actions = MagicMock()
    window.process_actions.kill = MagicMock()
    window.process_actions.open_location = MagicMock()

    window.selected_connection = None

    return window


def test_toggle_refresh_start():
    window = create_window()

    window.toggle_refresh(True)

    window.monitor.start.assert_called_once() # type: ignore


def test_toggle_refresh_running():
    window = create_window()

    window.monitor.isRunning.return_value = True # type: ignore

    window.toggle_refresh(True)

    window.monitor.start.assert_not_called() # type: ignore


def test_toggle_refresh_stop():
    window = create_window()

    window.toggle_refresh(False)

    window.monitor.stop.assert_called_once() # type: ignore


def test_kill_process():
    window = create_window()

    window.selected_connection = SimpleNamespace(pid=1234)

    window.kill_process()

    window.process_actions.kill.assert_called_once_with(1234) # type: ignore


def test_kill_process_without_selection():
    window = create_window()

    window.kill_process()

    window.process_actions.kill.assert_not_called() # type: ignore


def test_open_location():
    window = create_window()

    window.selected_connection = SimpleNamespace(
        path=r"C:\Program Files\App\app.exe"
    )

    window.open_location()

    window.process_actions.open_location.assert_called_once_with( # type: ignore
        r"C:\Program Files\App\app.exe"
    )


def test_open_location_without_selection():
    window = create_window()

    window.open_location()

    window.process_actions.open_location.assert_not_called() # type: ignore