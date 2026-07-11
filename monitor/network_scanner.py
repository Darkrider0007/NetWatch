"""
Network Scanner

Scans active TCP/UDP connections using psutil and
returns connection information for the GUI.
"""

from __future__ import annotations

from datetime import datetime

import psutil

from monitor.filters import (
    is_loopback,
    is_system_process,
)

from models.connection import ConnectionInfo
from models.settings import Settings
from services.dns_service import DNSService
from services.geoip_service import GeoIPService
from services.publisher_service import PublisherService
from services.process_service import ProcessService

from utils.logger import get_logger

logger = get_logger()


class NetworkScanner:

    def __init__(
        self,
        process_service=None,
        dns_service=None,
        geoip_service=None,
        publisher_service=None,
        settings=None,
    ):

        self._last_scan: list[ConnectionInfo] = []
        self.process_service = process_service or ProcessService()
        self.dns_service = dns_service or DNSService()
        self.geoip_service = geoip_service or GeoIPService()
        self.publisher_service = publisher_service or PublisherService()
        self.settings = settings or Settings()

    def scan(self) -> list[ConnectionInfo]:
        """
        Scan current network connections.

        Returns
        -------
        list[ConnectionInfo]
        """

        connections = []

        try:

            net_connections = psutil.net_connections(kind="inet")

        except Exception as exc:

            logger.exception(exc)

            return []

        for connection in net_connections:

            try:

                pid = connection.pid

                if pid is None:
                    continue

                process_name = self.process_service.get_name(pid)

                if is_system_process(process_name):
                    continue

                local_ip = ""
                local_port = 0

                remote_ip = ""
                remote_port = 0

                if connection.laddr:

                    local_ip = connection.laddr.ip
                    local_port = connection.laddr.port

                if connection.raddr:

                    remote_ip = connection.raddr.ip
                    remote_port = connection.raddr.port

                # Ignore localhost-only traffic
                if is_loopback(remote_ip):
                    continue

                protocol = "TCP"

                if connection.type == 2:
                    protocol = "UDP"

                executable = self.process_service.get_executable(pid)
                publisher = self.publisher_service.get_publisher(executable)

                if self.settings.resolve_dns:
                    hostname = (
                        self.dns_service.get(remote_ip)
                        or remote_ip
                    )
                else:
                    hostname = remote_ip

                country_code, country_name = self.geoip_service.country(remote_ip)

                item = ConnectionInfo(
                    time=datetime.now().strftime("%H:%M:%S"),
                    pid=pid,
                    process=process_name,
                    protocol=protocol,
                    local_ip=local_ip,
                    local_port=local_port,
                    remote_ip=remote_ip,
                    remote_port=remote_port,
                    remote_host=hostname,
                    status=connection.status,
                    path=executable,
                    publisher=publisher,
                    country_code=country_code,
                    country_name=country_name,
                )

                connections.append(item)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                AttributeError,
            ):

                continue

            except Exception as exc:

                logger.exception(exc)

        self._last_scan = connections

        return connections

    def last_scan(self) -> list[ConnectionInfo]:

        """
        Return previous scan.
        """

        return self._last_scan