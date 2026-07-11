from PySide6.QtWidgets import (
    QListWidget,
)


class DetailsPanel(QListWidget):

    def __init__(self):

        super().__init__()

    def update_statistics(
        self,
        stats,
    ):

        self.clear()
        self.addItem(
            f"Connections : {stats['total']}"
        )
        self.addItem("")
        self.addItem(
            "Top Processes"
        )
        for name, count in stats["processes"].most_common(5):
            self.addItem(
                f"{name} ({count})"
            )
        self.addItem("")
        self.addItem(
            "Top Countries"
        )
        for name, count in stats["countries"].most_common(5):
            self.addItem(
                f"{name} ({count})"
            )

    def update_connection(
        self,
        connection,
    ):

        self.clear()
        self.addItem(
            f"Process : {connection.process}"
        )
        self.addItem(
            f"Publisher : {connection.publisher}"
        )
        self.addItem(
            f"PID : {connection.pid}"
        )
        self.addItem(
            f"Protocol : {connection.protocol}"
        )
        self.addItem(
            f"Remote : {connection.remote_host}"
        )
        self.addItem(
            f"Country : {connection.country_name}"
        )
        self.addItem(
            f"Status : {connection.status}"
        )