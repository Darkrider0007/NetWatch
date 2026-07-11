from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QFileDialog,
    QSystemTrayIcon,
)
from PySide6.QtGui import QIcon

from config import (
    APP_NAME,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from gui.filter_bar import FilterBar
from gui.history_window import HistoryWindow
from gui.process_table import ProcessTable
from gui.details_panel import DetailsPanel
from gui.toolbar import MainToolBar
from gui.statusbar import MainStatusBar
from models.filter_state import FilterState
from monitor.connection_monitor import ConnectionMonitor
from services.browser_service import BrowserService
from services.dns_worker import DNSWorker
from services.history_service import HistoryService
from services.history_search import HistorySearch
from services.filter_service import FilterService
from services.export_service import ExportService
from gui.process_action_service import ProcessActionService
from services.notification_service import NotificationService
from services.statistics_service import StatisticsService
from services.settings_service import SettingsService

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(APP_NAME)

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
        )

        self.toolbar = MainToolBar()

        self.addToolBar(self.toolbar)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.windowIcon())
        self.tray.show()
        self.notification_service = NotificationService(
            self.tray
        )

        self.filter_state = FilterState()
        self.filter_service = FilterService()
        self.export_service = ExportService()
        self.history_service = HistoryService()
        self.process_actions = ProcessActionService()
        self.selected_connection = None
        self.history_window = HistoryWindow()
        self.history_search = HistorySearch()
        self.statistics = StatisticsService()
        self.settings_service = SettingsService()
        self.filter_bar = FilterBar()

        saved = self.settings_service.load()

        self.resize(
            saved.get("width", WINDOW_WIDTH),
            saved.get("height", WINDOW_HEIGHT),
        )

        self.filter_state.search = saved.get("search", "")
        self.filter_state.protocol = saved.get("protocol", "ALL")

        self.filter_bar.search.setText(self.filter_state.search)
        self.filter_bar.protocol.setCurrentText(self.filter_state.protocol)

        self.status = MainStatusBar()

        self.setStatusBar(self.status)

        self.table = ProcessTable()

        self.details = DetailsPanel()
        self.table.connection_selected.connect(
            self.connection_selected
        )
        self.table.menu.kill_requested.connect(
            self.kill_process
        )
        self.table.menu.open_location_requested.connect(
            self.open_location
        )

        central = QWidget()

        self.setCentralWidget(central)

        main_layout = QHBoxLayout()

        left = QVBoxLayout()

        left.addWidget(self.filter_bar)
        left.addWidget(self.table)

        main_layout.addLayout(left, 4)

        main_layout.addWidget(self.details, 1)

        central.setLayout(main_layout)

        self.monitor = ConnectionMonitor(interval=1)
        self.dns_worker = DNSWorker()

        self.filter_bar.search_changed.connect(
            lambda value: self.update_filter("search", value)
        )
        self.filter_bar.protocol_changed.connect(
            lambda value: self.update_filter("protocol", value)
        )
        self.filter_bar.country_changed.connect(
            lambda value: self.update_filter("country", value)
        )
        self.filter_bar.publisher_changed.connect(
            lambda value: self.update_filter("publisher", value)
        )
        self.filter_bar.established_changed.connect(
            lambda value: self.update_filter("established_only", value)
        )
        self.filter_bar.system_changed.connect(
            lambda value: self.update_filter("show_system", value)
        )

        self.toolbar.export_csv.connect(
            self.export_csv
        )
        self.toolbar.refresh_changed.connect(
            self.toggle_refresh
        )
        self.toolbar.history_clicked.connect(
            self.show_history
        )
        self.toolbar.clear_history.connect(
            self.clear_history
        )
        self.table.menu.virustotal_requested.connect(
            self.open_virustotal
        )
        self.table.menu.whois_requested.connect(
            self.open_whois
        )

        self.dns_worker.resolved.connect(
            self.hostname_resolved
        )
        self.monitor.connections_updated.connect(self.update_connections)
        self.monitor.monitor_error.connect(self.show_error)
        self.monitor.start()

    def toggle_refresh(
        self,
        enabled: bool,
    ):

        if enabled:
            if not self.monitor.isRunning():
                self.monitor.start()
        else:
            self.monitor.stop()

    def update_connections(self, changes):
        connections = self.filter_service.filter_connections(
            changes["current"],
            self.filter_state,
        )
        new_connections = changes.get("new", [])

        self.table.clear_connections()

        processes = set()

        for connection in connections:

            self.table.add_connection(connection)
            self.dns_worker.resolve(
                connection.remote_ip
            )

            processes.add(connection.pid)

        self.status.update_counts(
            len(connections),
            len(processes),
        )

        stats = self.statistics.build(connections)
        self.details.update_statistics(stats)

        for connection in new_connections:
            self.notification_service.notify(
                "New Connection",
                f"{connection.process} → {connection.remote_host}",
            )

        self.history_service.save(connections)

    def connection_selected(self, connection):

        self.selected_connection = connection
        self.details.update_connection(connection)

    def update_filter(
        self,
        field: str,
        value,
    ):

        setattr(
            self.filter_state,
            field,
            value,
        )
        self.update_connections(
            {
                "current": self.monitor.scanner.last_scan(),
            }
        )

    def export_csv(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "connections.csv",
            "CSV Files (*.csv)",
        )

        if not filename:
            return

        connections = self.filter_service.filter_connections(
            self.monitor.scanner.last_scan(),
            self.filter_state,
        )

        self.export_service.export_csv(
            connections,
            filename,
        )

        self.status.showMessage(
            f"Exported {len(connections)} connections.",
            5000,
        )

    def show_history(self):

        rows = self.history_search.search("")
        self.history_window.load(rows)
        self.history_window.show()

    def clear_history(self):

        self.history_service.clear()
        self.status.showMessage(
            "History cleared",
            3000,
        )

    def kill_process(self):

        if self.selected_connection:
            self.process_actions.kill(
                self.selected_connection.pid
            )

    def open_location(self):

        if self.selected_connection:
            self.process_actions.open_location(
                self.selected_connection.path
            )

    def open_virustotal(self):

        if self.selected_connection:
            BrowserService.virustotal(
                self.selected_connection.path
            )

    def open_whois(self):

        if self.selected_connection:
            BrowserService.whois(
                self.selected_connection.remote_ip
            )

    def show_error(self, message):

        self.statusBar().showMessage(
            message,
            5000,
        )

    def hostname_resolved(
        self,
        ip: str,
        hostname: str,
    ):

        self.monitor.scanner.dns_service.put(
            ip,
            hostname,
        )
        self.table.update_hostname(
            ip,
            hostname,
        )

    def closeEvent(self, event):

        self.settings_service.save({
            "width": self.width(),
            "height": self.height(),
            "search": self.filter_state.search,
            "protocol": self.filter_state.protocol,
        })

        if hasattr(self, "monitor"):

            self.monitor.stop()
            self.monitor.wait()

        event.accept()


if __name__ == "__main__":

    app = QApplication([])

    window = MainWindow()

    window.show()

    app.exec()