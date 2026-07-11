"""
Application Configuration
"""

from pathlib import Path

# -----------------------------------------------------
# Project Paths
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

LOG_DIR = BASE_DIR / "logs"
DB_DIR = BASE_DIR / "database"
RESOURCE_DIR = BASE_DIR / "resources"
ICON_DIR = BASE_DIR / "icons"

DATABASE_PATH = DB_DIR / "history.db"
LOG_FILE = LOG_DIR / "netwatch.log"

# -----------------------------------------------------
# Window
# -----------------------------------------------------

APP_NAME = "NetWatch"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 850

REFRESH_INTERVAL = 1000  # milliseconds

# -----------------------------------------------------
# Filters
# -----------------------------------------------------

SYSTEM_PROCESSES = {
    "system",
    "system idle process",
    "svchost.exe",
    "services.exe",
    "lsass.exe",
    "wininit.exe",
    "winlogon.exe",
    "csrss.exe",
    "smss.exe",
    "registry",
    "dwm.exe"
}