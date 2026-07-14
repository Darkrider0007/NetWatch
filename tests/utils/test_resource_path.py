from pathlib import Path
import sys

from utils.resource_path import resource_path


def test_resource_path_development(monkeypatch):

    monkeypatch.setattr(
        sys,
        "frozen",
        False,
        raising=False,
    )

    path = resource_path("assets/icon.ico")

    assert isinstance(path, Path)
    assert path.name == "icon.ico"
    assert "assets" in str(path)


def test_resource_path_frozen(monkeypatch):

    monkeypatch.setattr(
        sys,
        "frozen",
        True,
        raising=False,
    )

    monkeypatch.setattr(
        sys,
        "_MEIPASS",
        r"C:\Temp\App",
        raising=False,
    )

    path = resource_path("assets/icon.ico")

    assert path == Path(r"C:\Temp\App") / "assets/icon.ico"