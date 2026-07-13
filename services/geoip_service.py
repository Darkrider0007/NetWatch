"""
GeoIP Service
"""

from __future__ import annotations

import sys
from pathlib import Path

import geoip2.database


def resource_path(relative_path: str) -> Path:
    """
    Return the correct path for both development
    and PyInstaller executable.
    """

    if getattr(sys, "frozen", False):
        base_path = Path(getattr(sys, "_MEIPASS", ""))
    else:
        base_path = Path(__file__).parent.parent

    return base_path / relative_path


class GeoIPService:

    def __init__(self):

        database = resource_path(
            "resources/geoip/GeoLite2-Country.mmdb"
        )

        self.reader = geoip2.database.Reader(database)

        self.cache = {}

    def country(self, ip: str):

        if ip in self.cache:
            return self.cache[ip]

        try:

            response = self.reader.country(ip)

            result = (
                response.country.iso_code or "",
                response.country.name or "",
            )

        except Exception:

            result = (
                "",
                "",
            )

        self.cache[ip] = result

        return result

    def close(self):

        self.reader.close()