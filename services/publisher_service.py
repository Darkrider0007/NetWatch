"""
Publisher Service

Reads executable version information to determine the company name.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pefile


class PublisherService:

    @lru_cache(maxsize=512)
    def get_publisher(
        self,
        executable: str,
    ) -> str:

        if not executable:

            return ""

        path = Path(executable)

        if not path.exists():

            return ""

        try:

            pe = pefile.PE(executable)

            if not hasattr(pe, "FileInfo"):

                return ""

            for fileinfo in pe.FileInfo:

                if fileinfo.Key != b"StringFileInfo":

                    continue

                for table in fileinfo.StringTable:

                    entries = table.entries

                    company = entries.get(b"CompanyName")

                    if company:

                        if isinstance(company, bytes):

                            return company.decode(
                                "utf-8",
                                errors="ignore",
                            )

                        return str(company)

        except Exception:

            pass

        return ""