from PySide6.QtWidgets import QApplication

from services.icon_service import IconService


app = QApplication.instance()

if app is None:
    app = QApplication([])


def test_get_icon():

    service = IconService()

    icon = service.get_icon("")

    assert icon is not None