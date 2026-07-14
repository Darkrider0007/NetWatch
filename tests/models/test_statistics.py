import pytest

from models.statistics import Statistics


def test_statistics_defaults():

    stats = Statistics()

    assert stats.total_connections == 0
    assert stats.active_processes == 0
    assert stats.bytes_sent == 0
    assert stats.bytes_received == 0


def test_statistics_custom_values():

    stats = Statistics(
        total_connections=15,
        active_processes=4,
        bytes_sent=1024,
        bytes_received=2048,
    )

    assert stats.total_connections == 15
    assert stats.active_processes == 4
    assert stats.bytes_sent == 1024
    assert stats.bytes_received == 2048


def test_statistics_slots():

    stats = Statistics()

    assert hasattr(stats, "__slots__")

    with pytest.raises(AttributeError):
        setattr(stats, "new_attribute", 123)