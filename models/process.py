from dataclasses import dataclass


@dataclass(slots=True)
class ProcessInfo:

    pid: int

    name: str

    executable: str

    parent_pid: int | None = None

    username: str = ""

    publisher: str = ""