import os
import subprocess

import psutil


class ProcessActionService:

    def kill(self, pid):

        try:
            psutil.Process(pid).terminate()
        except Exception:
            pass

    def open_location(self, path):

        if path:
            subprocess.Popen(
                [
                    "explorer",
                    "/select,",
                    path,
                ]
            )

    def properties(self, path):

        if path:
            os.startfile(path)
