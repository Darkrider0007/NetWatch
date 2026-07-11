"""
GeoIP Service
"""

from __future__ import annotations

from pathlib import Path

import geoip2.database


class GeoIPService:

    def __init__(self):

        database = (
            Path(__file__)
            .parent.parent
            / "resources"
            / "geoip"
            / "GeoLite2-Country.mmdb"
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