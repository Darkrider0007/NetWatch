from PySide6.QtWidgets import (
    QStatusBar,
    QLabel,
)


class MainStatusBar(QStatusBar):

    def __init__(self):

        super().__init__()

        self.connection_label = QLabel("Connections : 0")

        self.process_label = QLabel("Processes : 0")

        self.addPermanentWidget(self.connection_label)

        self.addPermanentWidget(self.process_label)

    def update_counts(
        self,
        connections,
        processes,
    ):

        self.connection_label.setText(
            f"Connections : {connections}"
        )

        self.process_label.setText(
            f"Processes : {processes}"
        )