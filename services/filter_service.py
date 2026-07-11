"""
Filter Service

Filters ConnectionInfo objects according to the current filter state.
"""

from __future__ import annotations

from models.connection import ConnectionInfo
from models.filter_state import FilterState


class FilterService:

    def filter_connections(
        self,
        connections: list[ConnectionInfo],
        state: FilterState,
    ) -> list[ConnectionInfo]:

        filtered: list[ConnectionInfo] = []

        search = state.search.lower().strip()

        for connection in connections:

            #
            # Search
            #

            if search:

                searchable = " ".join(
                    [
                        connection.process,
                        connection.publisher,
                        connection.remote_host,
                        connection.remote_ip,
                        connection.local_ip,
                        connection.country_name,
                        str(connection.pid),
                        str(connection.remote_port),
                    ]
                ).lower()

                if search not in searchable:
                    continue

            #
            # Protocol
            #

            if (
                state.protocol != "ALL"
                and connection.protocol != state.protocol
            ):
                continue

            #
            # Country
            #

            if (
                state.country != "ALL"
                and connection.country_name != state.country
            ):
                continue

            #
            # Publisher
            #

            if (
                state.publisher != "ALL"
                and connection.publisher != state.publisher
            ):
                continue

            #
            # Established Only
            #

            if (
                state.established_only
                and connection.status != "ESTABLISHED"
            ):
                continue

            #
            # Passed all filters
            #

            filtered.append(connection)

        return filtered