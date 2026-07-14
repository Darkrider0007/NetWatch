from unittest.mock import MagicMock
from typing import Optional

from controllers.main_controller import MainController


def test_init():
    controller = MainController()

    assert controller.monitor is None


def test_start_without_monitor():
    controller = MainController()

    # Should not raise
    controller.start()


def test_stop_without_monitor():
    controller = MainController()

    # Should not raise
    controller.stop()


def test_start_with_monitor():
    controller = MainController()

    monitor: Optional[MagicMock] = MagicMock()

    controller.monitor = monitor  # type: ignore

    controller.start()

    monitor.start.assert_called_once()


def test_stop_with_monitor():
    controller = MainController()

    monitor: Optional[MagicMock] = MagicMock()

    controller.monitor = monitor  # type: ignore

    controller.stop()

    monitor.stop.assert_called_once()