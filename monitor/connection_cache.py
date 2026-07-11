"""
Connection Cache

Maintains the current set of active connections and computes
the differences between scans.
"""

from __future__ import annotations

from typing import Dict

from models.connection import ConnectionInfo


ConnectionKey = tuple[
    int,     # pid
    str,     # local_ip
    int,     # local_port
    str,     # remote_ip
    int,     # remote_port
    str,     # protocol
]


class ConnectionCache:

    def __init__(self):

        self._cache: Dict[
            ConnectionKey,
            ConnectionInfo,
        ] = {}

    @staticmethod
    def make_key(
        connection: ConnectionInfo,
    ) -> ConnectionKey:

        return (

            connection.pid,

            connection.local_ip,

            connection.local_port,

            connection.remote_ip,

            connection.remote_port,

            connection.protocol,
        )

    def compare(
        self,
        latest_connections: list[ConnectionInfo],
    ):

        latest: Dict[
            ConnectionKey,
            ConnectionInfo,
        ] = {}

        for connection in latest_connections:

            key = self.make_key(connection)

            latest[key] = connection

        added: list[ConnectionInfo] = []

        removed: list[ConnectionInfo] = []

        updated: list[ConnectionInfo] = []

        # New / Updated
        for key, value in latest.items():

            if key not in self._cache:

                added.append(value)

            elif value != self._cache[key]:

                updated.append(value)

        # Removed
        for key, value in self._cache.items():

            if key not in latest:

                removed.append(value)

        self._cache = latest

        return {

            "added": added,

            "removed": removed,

            "updated": updated,

            "current": latest_connections,
        }