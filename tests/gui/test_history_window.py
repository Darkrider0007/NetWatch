from gui.history_window import HistoryWindow


def test_creation(qtbot):
    window = HistoryWindow()

    qtbot.addWidget(window)

    assert window.windowTitle() == "Connection History"
    assert window.table.rowCount() == 0
    assert window.table.columnCount() == 0


def test_load_empty(qtbot):
    window = HistoryWindow()

    qtbot.addWidget(window)

    window.load([])

    assert window.table.rowCount() == 0
    assert window.table.columnCount() == 0


def test_load_rows(qtbot):
    window = HistoryWindow()

    qtbot.addWidget(window)

    rows = [
        (1, "chrome.exe", "8.8.8.8"),
        (2, "python.exe", "1.1.1.1"),
    ]

    window.load(rows)

    assert window.table.rowCount() == 2
    assert window.table.columnCount() == 3

    item = window.table.item(0, 0)
    assert item is not None
    assert item.text() == "1"
    item = window.table.item(0, 1)
    assert item is not None
    assert item.text() == "chrome.exe"
    item = window.table.item(0, 2)
    assert item is not None
    assert item.text() == "8.8.8.8"

    item = window.table.item(1, 0)
    assert item is not None
    assert item.text() == "2"
    item = window.table.item(1, 1)
    assert item is not None
    assert item.text() == "python.exe"
    item = window.table.item(1, 2)
    assert item is not None
    assert item.text() == "1.1.1.1"