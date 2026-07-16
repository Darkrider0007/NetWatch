from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
)


class SettingsDialog(QDialog):

    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.notifications = QCheckBox()
        self.notifications.setChecked(
            settings.get("notifications", True)
        )

        self.auto_refresh = QCheckBox()
        self.auto_refresh.setChecked(
            settings.get("auto_refresh", True)
        )

        self.refresh_interval = QComboBox()
        self.refresh_interval.addItems(
            [
                "1",
                "2",
                "5",
                "10",
            ]
        )

        interval = str(
            settings.get("refresh_interval", 1)
        )

        index = self.refresh_interval.findText(interval)

        if index >= 0:
            self.refresh_interval.setCurrentIndex(index)

        form.addRow(
            "Desktop Notifications",
            self.notifications,
        )

        form.addRow(
            "Auto Refresh",
            self.auto_refresh,
        )

        form.addRow(
            "Refresh Interval (sec)",
            self.refresh_interval,
        )

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def get_settings(self):

        return {
            "notifications": self.notifications.isChecked(),
            "auto_refresh": self.auto_refresh.isChecked(),
            "refresh_interval": int(
                self.refresh_interval.currentText()
            ),
        }