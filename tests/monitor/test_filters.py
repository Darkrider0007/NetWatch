from monitor.filters import (
    is_loopback,
    is_multicast,
    is_private,
    is_system_process,
)
from config import SYSTEM_PROCESSES


def test_is_system_process_true():

    if not SYSTEM_PROCESSES:
        return

    process = next(iter(SYSTEM_PROCESSES))

    assert is_system_process(process)


def test_is_system_process_false():

    assert is_system_process("my_custom_app.exe") is False


def test_is_private_true():

    assert is_private("192.168.1.1") is True
    assert is_private("10.0.0.1") is True
    assert is_private("172.16.0.1") is True


def test_is_private_false():

    assert is_private("8.8.8.8") is False


def test_is_private_invalid():

    assert is_private("invalid-ip") is True


def test_is_loopback_true():

    assert is_loopback("127.0.0.1") is True
    assert is_loopback("::1") is True


def test_is_loopback_false():

    assert is_loopback("8.8.8.8") is False


def test_is_loopback_invalid():

    assert is_loopback("invalid-ip") is True


def test_is_multicast_true():

    assert is_multicast("224.0.0.1") is True
    assert is_multicast("239.255.255.255") is True


def test_is_multicast_false():

    assert is_multicast("8.8.8.8") is False


def test_is_multicast_invalid():

    assert is_multicast("invalid-ip") is False