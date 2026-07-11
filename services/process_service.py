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
    def get_process_info(cls, pid: int) -> ProcessInfo | None:

        process = cls.get_process(pid)

        if process is None:

            return None

        try:

            return ProcessInfo(

                pid=pid,

                name=process.name(),

                executable=process.exe(),

                parent_pid=process.ppid(),

                username=process.username(),

            )

        except Exception:

            return None

    @classmethod
    def get_name(cls, pid: int) -> str:

        info = cls.get_process_info(pid)

        return info.name if info else "Unknown"

    @classmethod
    def get_executable(cls, pid: int) -> str:

        info = cls.get_process_info(pid)

        return info.executable if info else ""