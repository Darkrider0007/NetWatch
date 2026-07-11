"""
Filter Bar

Provides search and filtering controls.
"""

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
)


class FilterBar(QWidget):

    search_changed = Signal(str)

    protocol_changed = Signal(str)

    country_changed = Signal(str)

    publisher_changed = Signal(str)

    established_changed = Signal(bool)

    system_changed = Signal(bool)

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        #
        # Search
        #

        layout.addWidget(QLabel("Search"))

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Process, IP, Host..."
        )

        layout.addWidget(self.search)

        #
        # Protocol
        #

        layout.addWidget(QLabel("Protocol"))

        self.protocol = QComboBox()

        self.protocol.addItems(
            [
                "ALL",
                "TCP",
                "UDP",
            ]
        )

        layout.addWidget(self.protocol)

        #
        # Country
        #

        layout.addWidget(QLabel("Country"))

        self.country = QComboBox()

        self.country.addItem("ALL")

        layout.addWidget(self.country)

        #
        # Publisher
        #

        layout.addWidget(QLabel("Publisher"))

        self.publisher = QComboBox()

        self.publisher.addItem("ALL")

        layout.addWidget(self.publisher)

        #
        # Established
        #

        self.established = QCheckBox(
            "Established Only"
        )

        layout.addWidget(self.established)

        #
        # System
        #

        self.system = QCheckBox(
            "Show System"
        )

        layout.addWidget(self.system)

        layout.addStretch()

        #
        # Signals
        #

        self.search.textChanged.connect(
            self.search_changed.emit
        )

        self.protocol.currentTextChanged.connect(
            self.protocol_changed.emit
        )

        self.country.currentTextChanged.connect(
            self.country_changed.emit
        )

        self.publisher.currentTextChanged.connect(
            self.publisher_changed.emit
        )

        self.established.toggled.connect(
            self.established_changed.emit
        )

        self.system.toggled.connect(
            self.system_changed.emit
        )

    def set_countries(
        self,
        countries: list[str],
    ):

        current = self.country.currentText()

        self.country.blockSignals(True)

        self.country.clear()

        self.country.addItem("ALL")

        self.country.addItems(sorted(countries))

        index = self.country.findText(current)

        if index >= 0:

            self.country.setCurrentIndex(index)

        self.country.blockSignals(False)

    def set_publishers(
        self,
        publishers: list[str],
    ):

        current = self.publisher.currentText()

        self.publisher.blockSignals(True)

        self.publisher.clear()

        self.publisher.addItem("ALL")

        self.publisher.addItems(sorted(publishers))

        index = self.publisher.findText(current)

        if index >= 0:

            self.publisher.setCurrentIndex(index)

        self.publisher.blockSignals(False)