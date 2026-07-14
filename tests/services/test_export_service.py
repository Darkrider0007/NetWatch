import csv

from models.connection import ConnectionInfo
from services.export_service import ExportService


def test_export_csv(tmp_path):
    file = tmp_path / "connections.csv"

    conn = ConnectionInfo(
        time="12",
        pid=1,
        process="chrome",
        protocol="TCP",
        local_ip="1",
        local_port=1,
        remote_ip="8.8.8.8",
        remote_port=443,
        remote_host="google",
        status="ESTABLISHED",
        path="c:/chrome.exe",
    )

    ExportService().export_csv([conn], file)

    assert file.exists()

    with open(file, newline="", encoding="utf8") as f:
        rows = list(csv.reader(f))

    assert len(rows) >= 2