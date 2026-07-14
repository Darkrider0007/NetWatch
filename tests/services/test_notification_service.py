from unittest.mock import MagicMock

from PySide6.QtWidgets import QSystemTrayIcon

from services.notification_service import NotificationService


def test_notify_supported():

    tray = MagicMock(spec=QSystemTrayIcon)

    tray.supportsMessages.return_value = True

    service = NotificationService(tray)

    service.notify(
        "Test Title",
        "Test Message",
    )

    tray.showMessage.assert_called_once_with(
        "Test Title",
        "Test Message",
        QSystemTrayIcon.MessageIcon.Information,
        3000,
    )


def test_notify_not_supported():

    tray = MagicMock(spec=QSystemTrayIcon)

    tray.supportsMessages.return_value = False

    service = NotificationService(tray)

    service.notify(
        "Test Title",
        "Test Message",
    )

    tray.showMessage.assert_not_called()


def test_tray_is_saved():

    tray = MagicMock(spec=QSystemTrayIcon)

    service = NotificationService(tray)

    assert service.tray is tray