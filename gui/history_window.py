from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)


class HistoryWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Connection History")

        layout = QVBoxLayout(self)

        self.table = QTableWidget()

        layout.addWidget(self.table)

    def load(self, rows):

        if not rows:

            return

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(len(rows[0]))

        for r, row in enumerate(rows):

            for c, value in enumerate(row):

                self.table.setItem(
                    r,
                    c,
                    QTableWidgetItem(str(value)),
                )