"""
Icon Service

Provides cached file icons using the native Windows icon provider.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtCore import QFileInfo


class IconService:

    def __init__(self):

        self._provider = QFileIconProvider()

        self._default = QIcon()

    @lru_cache(maxsize=512)
    def get_icon(
        self,
        executable: str,
    ) -> QIcon:

        if not executable:

            return self._default

        executable = str(Path(executable))

        info = QFileInfo(executable)

        return self._provider.icon(info)