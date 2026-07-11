"""
Background thread for monitoring network connections.
"""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal

from monitor.connection_cache import ConnectionCache
from monitor.network_scanner import NetworkScanner
from utils.logger import get_logger

logger = get_logger()


class ConnectionMonitor(QThread):
    """
    Background monitoring thread.
    """

    # Emits the latest list of connections
    connections_updated = Signal(dict)

    # Emits any fatal error
    monitor_error = Signal(str)

    def __init__(self, interval: float = 1.0):

        super().__init__()

        self.interval = interval

        self.scanner = NetworkScanner()

        self._running = True

        self.cache = ConnectionCache()

    def stop(self):
        """
        Stop monitoring thread.
        """

        logger.info("Stopping monitor thread...")

        self._running = False

    def run(self):

        logger.info("Connection monitor started.")

        while self._running:

            try:

                latest = self.scanner.scan()

                changes = self.cache.compare(latest)

                self.connections_updated.emit(changes)

            except Exception as exc:

                logger.exception(exc)

                self.monitor_error.emit(str(exc))

            self.msleep(int(self.interval * 1000))

        logger.info("Connection monitor stopped.")