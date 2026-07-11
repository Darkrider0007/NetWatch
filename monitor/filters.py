import ipaddress

from config import SYSTEM_PROCESSES


def is_system_process(name: str) -> bool:

    return name.lower() in SYSTEM_PROCESSES


def is_private(ip: str) -> bool:

    try:

        return ipaddress.ip_address(ip).is_private

    except ValueError:

        return True


def is_loopback(ip: str) -> bool:

    try:

        return ipaddress.ip_address(ip).is_loopback

    except ValueError:

        return True


def is_multicast(ip: str) -> bool:

    try:

        return ipaddress.ip_address(ip).is_multicast

    except ValueError:

        return False