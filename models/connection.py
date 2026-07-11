from dataclasses import dataclass


@dataclass(slots=True)
class ConnectionInfo:

    time: str

    pid: int

    process: str

    protocol: str

    local_ip: str

    local_port: int

    remote_ip: str

    remote_port: int

    remote_host: str

    status: str

    path: str

    bytes_sent: int = 0

    bytes_received: int = 0

    packets_sent: int = 0

    packets_received: int = 0

    publisher: str = ""

    country_code: str = ""

    country_name: str = ""

    def __getitem__(self, key: str):

        return getattr(self, key)