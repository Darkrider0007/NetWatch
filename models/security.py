from dataclasses import dataclass, field


@dataclass(slots=True)
class SecurityReport:

    process: str

    publisher: str

    digital_signature: str

    sha256: str

    file_size_bytes: int

    file_size_display: str

    path: str

    connections: int

    remote_countries: list[str] = field(default_factory=list)

    signer: str = ""

    signature_status: str = ""

    generated_at: str = ""

    def to_dict(self) -> dict:

        return {
            "process": self.process,
            "publisher": self.publisher,
            "digital_signature": self.digital_signature,
            "sha256": self.sha256,
            "file_size_bytes": self.file_size_bytes,
            "file_size": self.file_size_display,
            "path": self.path,
            "connections": self.connections,
            "remote_countries": self.remote_countries,
            "signer": self.signer,
            "signature_status": self.signature_status,
            "generated_at": self.generated_at,
        }