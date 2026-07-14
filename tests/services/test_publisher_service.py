from unittest.mock import MagicMock, patch

from services.publisher_service import PublisherService


@patch("services.publisher_service.Path.exists")
@patch("services.publisher_service.pefile.PE")
def test_get_publisher(
    mock_pe,
    mock_exists,
):
    mock_exists.return_value = True

    table = MagicMock()

    table.entries = {
        b"CompanyName": b"Microsoft"
    }

    string_info = MagicMock()

    string_info.Key = b"StringFileInfo"
    string_info.StringTable = [table]

    pe = MagicMock()

    pe.FileInfo = [string_info]

    mock_pe.return_value = pe

    publisher = PublisherService()

    assert (
        publisher.get_publisher("test.exe")
        == "Microsoft"
    )


def test_empty_path():

    publisher = PublisherService()

    assert publisher.get_publisher("") == ""