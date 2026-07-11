"""
Background DNS resolver.
"""

from __future__ import annotations

import socket
from queue import Queue, Empty
from threading import Thread

from PySide6.QtCore import QObject, Signal


class DNSWorker(QObject):

    resolved = Signal(str, str)

    def __init__(self):

        super().__init__()

        self.queue = Queue()

        self.cache = {}

        self._worker_thread = Thread(
            target=self._run,
            daemon=True,
        )

        self._worker_thread.start()

    def resolve(self, ip: str):

        if not ip:
            return

        if ip in self.cache:

            self.resolved.emit(
                ip,
                self.cache[ip],
            )

            return

        self.queue.put(ip)

    def _run(self):

        while True:

            try:

                ip = self.queue.get(timeout=1)

            except Empty:

                continue

            try:

                hostname = socket.gethostbyaddr(ip)[0]

            except Exception:

                hostname = ip

            self.cache[ip] = hostname

            self.resolved.emit(
                ip,
                hostname,
            )