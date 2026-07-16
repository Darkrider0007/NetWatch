from PySide6.QtWidgets import QApplication

from gui.settings_dialog import SettingsDialog


def get_app():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    return app


def test_default_settings():

    get_app()

    dialog = SettingsDialog({})

    settings = dialog.get_settings()

    assert settings["notifications"] is True
    assert settings["auto_refresh"] is True
    assert settings["refresh_interval"] == 1


def test_load_existing_settings():

    get_app()

    dialog = SettingsDialog(
        {
            "notifications": False,
            "auto_refresh": False,
            "refresh_interval": 5,
        }
    )

    settings = dialog.get_settings()

    assert settings == {
        "notifications": False,
        "auto_refresh": False,
        "refresh_interval": 5,
    }


def test_change_settings():

    get_app()

    dialog = SettingsDialog({})

    dialog.notifications.setChecked(False)
    dialog.auto_refresh.setChecked(False)
    dialog.refresh_interval.setCurrentText("10")

    settings = dialog.get_settings()

    assert settings == {
        "notifications": False,
        "auto_refresh": False,
        "refresh_interval": 10,
    }


def test_window_properties():

    get_app()

    dialog = SettingsDialog({})

    assert dialog.windowTitle() == "Settings"

    assert dialog.minimumWidth() == 350