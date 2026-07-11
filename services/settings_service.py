import json
from pathlib import Path


class SettingsService:

    FILE = Path("settings.json")

    def save(self, settings):

        with open(self.FILE, "w") as f:

            json.dump(settings, f, indent=4)

    def load(self):

        if not self.FILE.exists():

            return {}

        with open(self.FILE) as f:

            return json.load(f)