from PySide6.QtWidgets import (
    QToolBar,
)

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction


class MainToolBar(QToolBar):

    export_csv = Signal()
    refresh_changed = Signal(bool)
    history_clicked = Signal()
    clear_history = Signal()
    settings_clicked = Signal()

    def __init__(self):

        super().__init__("Toolbar")

        self.refresh_action = QAction("Refresh")

        self.clear_action = QAction("Clear")

        self.export_action = QAction("Export CSV")

        self.settings_action = QAction("Settings")

        self.settings_action.triggered.connect(
            self.settings_clicked.emit
        )

        self.addAction(self.refresh_action)

        self.addSeparator()

        self.addAction(self.clear_action)

        self.addSeparator()

        self.addAction(self.export_action)
        self.export_action.triggered.connect(
            self.export_csv.emit
        )

        self.history_action = self.addAction("History")
        self.history_action.triggered.connect(
            self.history_clicked.emit
        )

        self.clear_action = self.addAction(
            "Clear History"
        )
        self.clear_action.triggered.connect(
            self.clear_history.emit
        )

        self.auto_refresh = self.addAction("Auto Refresh")
        self.auto_refresh.setCheckable(True)
        self.auto_refresh.setChecked(True)
        self.auto_refresh.toggled.connect(
            self.refresh_changed.emit
        )

        self.addSeparator()

        self.addAction(self.settings_action)