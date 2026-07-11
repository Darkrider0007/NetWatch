from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from gui.context_menu import ConnectionContextMenu
from models.connection import ConnectionInfo
from services.icon_service import IconService


class ProcessTable(QTableWidget):
    """
    Main table displaying live network connections.
    """

    connection_selected = Signal(object)

    COL_TIME = 0
    COL_PROCESS = 1
    COL_PUBLISHER = 2
    COL_PID = 3
    COL_PROTOCOL = 4
    COL_LOCAL = 5
    COL_REMOTE = 6
    COL_COUNTRY = 7
    COL_PORT = 8
    COL_STATUS = 9

    HEADERS = [
        "Time",
        "Process",
        "Publisher",
        "PID",
        "Protocol",
        "Local",
        "Remote",
        "Country",
        "Port",
        "Status",
    ]

    def __init__(self):

        super().__init__()

        self.setSortingEnabled(True)

        self.icon_service = IconService()

        self.setColumnCount(len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)

        self.setAlternatingRowColors(True)

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.itemSelectionChanged.connect(
            self.selection_changed
        )
        self.customContextMenuRequested.connect(
            self.show_menu
        )

        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(28)

        header = self.horizontalHeader()
        header.setStretchLastSection(False)
        for column in range(self.columnCount()):

            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeMode.ResizeToContents,
            )

        header.setSectionResizeMode(
            self.COL_PUBLISHER,
            QHeaderView.ResizeMode.Stretch,
        )

        self.connection_rows = {}
        self.menu = ConnectionContextMenu(self)

    def make_key(
        self,
        pid: int,
        local_ip: str,
        remote_ip: str,
        remote_port: int,
        protocol: str,
    ):

        return (
            pid,
            local_ip,
            remote_ip,
            remote_port,
            protocol,
        )

    def add_connection(
        self,
        connection: ConnectionInfo,
    ):

        row = self.rowCount()
        self.insertRow(row)

        time_item = QTableWidgetItem(connection.time)
        time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 0, time_item)

        icon = self.icon_service.get_icon(connection.path)
        process_item = QTableWidgetItem(icon, connection.process)
        process_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 1, process_item)

        values = [
            connection.publisher,
            str(connection.pid),
            connection.protocol,
            connection.local_ip,
            connection.remote_host,
            connection.country_name,
            str(connection.remote_port),
            connection.status,
        ]

        for column, value in enumerate(values, start=2):

            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.setItem(
                row,
                column,
                item,
            )

        key = self.make_key(
            connection.pid,
            connection.local_ip,
            connection.remote_ip,
            connection.remote_port,
            connection.protocol,
        )

        self.connection_rows[key] = (row, connection)

    def clear_connections(self):

        self.connection_rows.clear()
        self.setRowCount(0)

    def selection_changed(self):

        rows = self.selectionModel().selectedRows()

        if not rows:
            return

        row = rows[0].row()

        for _, value in self.connection_rows.items():

            r, connection = value

            if r == row:
                self.connection_selected.emit(connection)
                return

    def show_menu(self, pos):

        self.menu.exec(
            self.viewport().mapToGlobal(pos)
        )

    def update_hostname(
        self,
        ip: str,
        hostname: str,
    ):

        for row in range(self.rowCount()):

            remote_item = self.item(row, self.COL_REMOTE)

            if remote_item is None:
                continue

            if remote_item.text() == ip:
                remote_item.setText(hostname)