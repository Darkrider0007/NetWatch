"""
Desktop Notification Service
"""

from PySide6.QtWidgets import QSystemTrayIcon


class NotificationService:

    def __init__(self, tray: QSystemTrayIcon):

        self.tray = tray

    def notify(self, title: str, message: str):

        if self.tray.supportsMessages():

            self.tray.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                3000,
            )