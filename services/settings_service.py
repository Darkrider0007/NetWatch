import json
from pathlib import Path


class SettingsService:

    FILE = Path("settings.json")

    DEFAULTS = {
        "notifications": True,
        "auto_refresh": True,
        "refresh_interval": 1,
        "width": 1400,
        "height": 800,
        "search": "",
        "protocol": "ALL",
    }

    def save(self, settings):

        with open(self.FILE, "w") as f:

            json.dump(settings, f, indent=4)

    def load(self):

        if not self.FILE.exists():

            return self.DEFAULTS.copy()

        with open(self.FILE) as f:

            settings = json.load(f)

        merged = self.DEFAULTS.copy()
        merged.update(settings)

        return merged