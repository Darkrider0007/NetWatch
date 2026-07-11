from dataclasses import dataclass


@dataclass(slots=True)
class Statistics:

    total_connections: int = 0

    active_processes: int = 0

    bytes_sent: int = 0

    bytes_received: int = 0