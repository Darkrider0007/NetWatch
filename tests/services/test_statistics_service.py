from services.statistics_service import StatisticsService
from models.connection import ConnectionInfo


def connection(process, country):
    return ConnectionInfo(
        time="12",
        pid=1,
        process=process,
        protocol="TCP",
        local_ip="1",
        local_port=1,
        remote_ip="2",
        remote_port=80,
        remote_host="host",
        status="ESTABLISHED",
        path="c:/a.exe",
        country_name=country,
    )


def test_statistics_empty():
    stats = StatisticsService().build([])

    assert stats["total"] == 0
    assert len(stats["processes"]) == 0
    assert len(stats["countries"]) == 0


def test_statistics_counts():
    service = StatisticsService()

    stats = service.build(
        [
            connection("chrome", "US"),
            connection("chrome", "US"),
            connection("edge", "IN"),
        ]
    )

    assert stats["total"] == 3
    assert stats["processes"]["chrome"] == 2
    assert stats["countries"]["US"] == 2