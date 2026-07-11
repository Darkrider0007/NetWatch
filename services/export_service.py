"""
CSV Export Service
"""

from __future__ import annotations

import csv
from pathlib import Path

from models.connection import ConnectionInfo


class ExportService:

    def export_csv(
        self,
        connections: list[ConnectionInfo],
        filename: str,
    ):

        Path(filename).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Time",
                "Process",
                "Publisher",
                "PID",
                "Protocol",
                "Local IP",
                "Local Port",
                "Remote Host",
                "Remote IP",
                "Remote Port",
                "Country",
                "Status",
            ])

            for c in connections:

                writer.writerow([
                    c.time,
                    c.process,
                    c.publisher,
                    c.pid,
                    c.protocol,
                    c.local_ip,
                    c.local_port,
                    c.remote_host,
                    c.remote_ip,
                    c.remote_port,
                    c.country_name,
                    c.status,
                ])