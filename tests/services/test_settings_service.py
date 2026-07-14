from services.settings_service import SettingsService


def test_save_and_load(tmp_path, monkeypatch):
    settings_file = tmp_path / "settings.json"

    monkeypatch.setattr(
        SettingsService,
        "FILE",
        settings_file,
    )

    service = SettingsService()

    data = {
        "width": 100,
        "height": 200,
    }

    service.save(data)

    loaded = service.load()

    assert loaded == data


def test_load_missing_file(tmp_path, monkeypatch):
    settings_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        SettingsService,
        "FILE",
        settings_file,
    )

    service = SettingsService()

    assert service.load() == {}