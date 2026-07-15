"""
Process Service

Provides process-related information using psutil.
"""

from __future__ import annotations

import psutil

from models.process import ProcessInfo


class ProcessService:

    @staticmethod
    def get_process(pid: int):

        try:

            return psutil.Process(pid)

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):

            return None

    @classmethod
    def get_process_info(
        cls,
        pid: int,
    ) -> ProcessInfo | None:

        process = cls.get_process(pid)

        if process is None:

            return None

        try:
            name = process.name()
        except Exception:
            name = "Unknown"

        try:
            executable = process.exe()
        except Exception:
            executable = ""

        try:
            parent_pid = process.ppid()
        except Exception:
            parent_pid = 0

        try:
            username = process.username()
        except Exception:
            username = ""

        return ProcessInfo(
            pid=pid,
            name=name,
            executable=executable,
            parent_pid=parent_pid,
            username=username,
        )

    @classmethod
    def get_name(
        cls,
        pid: int,
    ) -> str:

        info = cls.get_process_info(pid)

        if info is None:

            return "Unknown"

        return info.name

    @classmethod
    def get_executable(
        cls,
        pid: int,
    ) -> str:

        info = cls.get_process_info(pid)

        if info is None:

            return ""

        return info.executable