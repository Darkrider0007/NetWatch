import os
import subprocess

import psutil

from monitor.protected_processes import SYSTEM_PROCESSES


class ProcessActionService:

    def kill(self, pid):

        try:
            process = psutil.Process(pid)

        except psutil.NoSuchProcess:
            return (
                False,
                "Process no longer exists.",
            )

        except psutil.AccessDenied:
            return (
                False,
                "Access denied. Run NetWatch as Administrator.",
            )

        try:

            #
            # Find the root process (Chrome/Brave/VSCode/Electron apps)
            #
            root = process

            while True:

                try:
                    parent = root.parent()

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                ):
                    break

                if parent is None:
                    break

                try:
                    if (
                        parent.name().lower()
                        != root.name().lower()
                    ):
                        break

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                ):
                    break

                root = parent

            #
            # Don't allow terminating protected Windows processes
            #
            if root.name().lower() in SYSTEM_PROCESSES:

                return (
                    False,
                    f"{root.name()} is a protected Windows process.",
                )

            #
            # Get the entire process tree
            #
            children = root.children(recursive=True)

            #
            # Kill children first
            #
            for child in reversed(children):

                try:
                    child.kill()

                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                ):
                    pass

            #
            # Kill the root process
            #
            try:
                root.kill()

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):
                pass

            #
            # Wait for everything to exit
            #
            _, alive = psutil.wait_procs(
                [root] + children,
                timeout=5,
            )

            if alive:

                return (
                    False,
                    f"Unable to terminate {len(alive)} process(es). Administrator privileges may be required.",
                )

            return (
                True,
                f"{root.name()} terminated successfully.",
            )

        except psutil.AccessDenied:

            return (
                False,
                "Access denied. Run NetWatch as Administrator.",
            )

        except Exception as exc:

            return (
                False,
                str(exc),
            )

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