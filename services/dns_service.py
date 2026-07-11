"""
DNS Cache Service
"""

from __future__ import annotations


class DNSService:

    def __init__(self):

        self.cache = {}

    def get(self, ip: str):

        return self.cache.get(ip)

    def put(
        self,
        ip: str,
        hostname: str,
    ):

        self.cache[ip] = hostname