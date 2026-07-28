"""
Security Analysis Service

Collects security-related information about an executable:

- Process information
- Publisher
- SHA-256 hash
- File size
- Windows Authenticode signature
- Signer
- Network connection count
- Remote countries
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

from models.connection import ConnectionInfo
from models.security import SecurityReport
from services.publisher_service import PublisherService


class SecurityService:

    CHUNK_SIZE = 1024 * 1024

    def __init__(
        self,
        publisher_service: PublisherService | None = None,
    ):

        self.publisher_service = (
            publisher_service
            or PublisherService()
        )

    def analyze(
        self,
        path: str,
        process: str = "",
        connections: list[ConnectionInfo] | None = None,
    ) -> SecurityReport:

        executable = Path(path)

        publisher = self.publisher_service.get_publisher(
            str(executable)
        )

        sha256 = self.calculate_sha256(
            executable
        )

        file_size_bytes = self.get_file_size(
            executable
        )

        signature_status, signer = (
            self.get_digital_signature(
                executable
            )
        )

        process_connections = self.get_process_connections(
            connections or [],
            process=process,
            path=str(executable),
        )

        countries = self.get_remote_countries(
            process_connections
        )

        return SecurityReport(
            process=process or executable.name,
            publisher=publisher or "Unknown",
            digital_signature=self.format_signature_status(
                signature_status
            ),
            sha256=sha256,
            file_size_bytes=file_size_bytes,
            file_size_display=self.format_file_size(
                file_size_bytes
            ),
            path=str(executable),
            connections=len(process_connections),
            remote_countries=countries,
            signer=signer,
            signature_status=signature_status,
            generated_at=datetime.now().isoformat(
                timespec="seconds"
            ),
        )

    @classmethod
    def calculate_sha256(
        cls,
        path: Path,
    ) -> str:

        if not path.exists() or not path.is_file():
            return ""

        digest = hashlib.sha256()

        try:

            with path.open("rb") as file:

                while True:

                    chunk = file.read(
                        cls.CHUNK_SIZE
                    )

                    if not chunk:
                        break

                    digest.update(chunk)

            return digest.hexdigest().upper()

        except (
            OSError,
            PermissionError,
        ):

            return ""

    @staticmethod
    def get_file_size(
        path: Path,
    ) -> int:

        try:

            return path.stat().st_size

        except (
            OSError,
            PermissionError,
        ):

            return 0

    @staticmethod
    def format_file_size(
        size: int,
    ) -> str:

        if size < 1024:

            return f"{size} B"

        if size < 1024 ** 2:

            return f"{size / 1024:.1f} KB"

        if size < 1024 ** 3:

            value = size / (1024 ** 2)

            if value.is_integer():

                return f"{int(value)} MB"

            return f"{value:.1f} MB"

        value = size / (1024 ** 3)

        if value.is_integer():

            return f"{int(value)} GB"

        return f"{value:.2f} GB"

    @staticmethod
    def get_digital_signature(
        path: Path,
    ) -> tuple[str, str]:

        if not path.exists() or not path.is_file():
            return (
                "FileNotFound",
                "",
            )

        if os.name != "nt":
            return (
                "Unsupported",
                "",
            )

        script = r"""
$ErrorActionPreference = "Stop"

$path = [Environment]::GetEnvironmentVariable(
    "NETWATCH_SECURITY_PATH"
)

if (-not $path) {
    throw "Target path was not supplied."
}

if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Target file does not exist."
}

$signature = Get-AuthenticodeSignature -LiteralPath $path

$signer = ""

if ($null -ne $signature.SignerCertificate) {
    $signer = $signature.SignerCertificate.Subject
}

$result = [PSCustomObject]@{
    Status = [string]$signature.Status
    Signer = $signer
}

$result | ConvertTo-Json -Compress
"""

        environment = os.environ.copy()

        environment[
            "NETWATCH_SECURITY_PATH"
        ] = str(path)

        try:

            result = subprocess.run(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    script,
                ],
                capture_output=True,
                text=True,
                timeout=15,
                env=environment,
                creationflags=(
                    getattr(
                        subprocess,
                        "CREATE_NO_WINDOW",
                        0,
                    )
                ),
            )

        except (
            FileNotFoundError,
            subprocess.TimeoutExpired,
            OSError,
        ):

            return (
                "Unknown",
                "",
            )

        if result.returncode != 0:
            return (
                "Unknown",
                "",
            )

        try:

            data = json.loads(
                result.stdout.strip()
            )

        except (
            json.JSONDecodeError,
            ValueError,
        ):

            return (
                "Unknown",
                "",
            )

        status = str(
            data.get(
                "Status",
                "Unknown",
            )
        )

        signer = str(
            data.get(
                "Signer",
                "",
            )
        )

        return (
            status,
            signer,
        )

    @staticmethod
    def format_signature_status(
        status: str,
    ) -> str:

        normalized = status.lower()

        if normalized == "valid":
            return "✓ Valid"

        if normalized == "notsigned":
            return "⚠ Not Signed"

        if normalized == "hashmismatch":
            return "✕ Hash Mismatch"

        if normalized == "nottrusted":
            return "✕ Not Trusted"

        if normalized == "filemissing":
            return "✕ File Not Found"

        if normalized == "unsupported":
            return "⚠ Unsupported"

        return "⚠ Unknown"

    @staticmethod
    def get_process_connections(
        connections: list[ConnectionInfo],
        process: str = "",
        path: str = "",
    ) -> list[ConnectionInfo]:

        if not connections:
            return []

        process_name = process.lower().strip()
        executable = path.lower().strip()

        result = []

        for connection in connections:

            if process_name:

                if (
                    connection.process.lower()
                    == process_name
                ):
                    result.append(connection)

                    continue

            if executable and connection.path:

                if (
                    connection.path.lower()
                    == executable
                ):
                    result.append(connection)

        return result

    @staticmethod
    def get_remote_countries(
        connections: list[ConnectionInfo],
    ) -> list[str]:

        countries = set()

        for connection in connections:

            country = (
                connection.country_code
                or connection.country_name
            )

            if country:
                countries.add(country)

        return sorted(
            countries,
            key=str.upper,
        )

    @staticmethod
    def export_report(
        report: SecurityReport,
        filename: str,
    ) -> None:

        output = Path(filename)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report.to_dict(),
                file,
                indent=4,
                ensure_ascii=False,
            )