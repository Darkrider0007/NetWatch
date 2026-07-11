from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMenu


class ConnectionContextMenu(QMenu):

    kill_requested = Signal()
    open_location_requested = Signal()
    properties_requested = Signal()
    virustotal_requested = Signal()
    whois_requested = Signal()

    def __init__(self, parent=None):

        super().__init__(parent)

        self.addAction("Kill Process").triggered.connect(
            self.kill_requested.emit
        )

        self.addAction("Open File Location").triggered.connect(
            self.open_location_requested.emit
        )

        self.addAction("Properties").triggered.connect(
            self.properties_requested.emit
        )

        self.addSeparator()

        self.addAction("VirusTotal").triggered.connect(
            self.virustotal_requested.emit
        )

        self.addAction("Whois Lookup").triggered.connect(
            self.whois_requested.emit
        )