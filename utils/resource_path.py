from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    """
    Returns the correct path in both development
    and PyInstaller executable.
    """

    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative_path  # type: ignore[attr-defined]

    return Path(__file__).parent.parent / relative_path