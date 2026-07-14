import pytest
from PySide6.QtWidgets import QApplication

from gui.toolbar import MainToolBar


@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


def test_toolbar_creation(app):
    toolbar = MainToolBar()

    assert toolbar.windowTitle() == "Toolbar"


def test_export_action_exists(app):
    toolbar = MainToolBar()

    assert toolbar.export_action is not None
    assert toolbar.export_action.text() == "Export CSV"


def test_settings_action_exists(app):
    toolbar = MainToolBar()

    assert toolbar.settings_action is not None
    assert toolbar.settings_action.text() == "Settings"


def test_auto_refresh_defaults_enabled(app):
    toolbar = MainToolBar()

    assert toolbar.auto_refresh.isCheckable()
    assert toolbar.auto_refresh.isChecked()


def test_refresh_signal(app, qtbot):
    toolbar = MainToolBar()

    with qtbot.waitSignal(toolbar.refresh_changed):
        toolbar.auto_refresh.setChecked(False)


def test_refresh_signal_true(app, qtbot):
    toolbar = MainToolBar()

    toolbar.auto_refresh.setChecked(False)

    with qtbot.waitSignal(toolbar.refresh_changed):
        toolbar.auto_refresh.setChecked(True)


def test_export_signal(app, qtbot):
    toolbar = MainToolBar()

    with qtbot.waitSignal(toolbar.export_csv):
        toolbar.export_action.trigger()


def test_history_signal(app, qtbot):
    toolbar = MainToolBar()

    with qtbot.waitSignal(toolbar.history_clicked):
        toolbar.history_action.trigger()


def test_clear_history_signal(app, qtbot):
    toolbar = MainToolBar()

    with qtbot.waitSignal(toolbar.clear_history):
        toolbar.clear_action.trigger()


def test_toolbar_contains_actions(app):
    toolbar = MainToolBar()

    actions = toolbar.actions()

    texts = [
        action.text()
        for action in actions
        if action.text()
    ]

    assert "Export CSV" in texts
    assert "History" in texts
    assert "Clear History" in texts
    assert "Auto Refresh" in texts
    assert "Settings" in texts


def test_auto_refresh_toggle(app):
    toolbar = MainToolBar()

    toolbar.auto_refresh.setChecked(False)

    assert not toolbar.auto_refresh.isChecked()

    toolbar.auto_refresh.setChecked(True)

    assert toolbar.auto_refresh.isChecked()


def test_toolbar_action_count(app):
    toolbar = MainToolBar()

    assert len(toolbar.actions()) >= 6