from dataclasses import dataclass


@dataclass(slots=True)
class Settings:

    refresh_interval: int = 1000

    resolve_dns: bool = False

    show_system_processes: bool = False

    show_private_network: bool = False

    auto_scroll: bool = True