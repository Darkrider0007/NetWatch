from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from models.connection import ConnectionInfo
from models.security import SecurityReport
from services.browser_service import BrowserService
from services.security_service import SecurityService


class SecurityDialog(QDialog):

    def __init__(
        self,
        path: str,
        process: str,
        connections: list[ConnectionInfo] | None = None,
        parent=None,
    ):

        super().__init__(parent)

        self.path = path
        self.process = process
        self.connections = connections or []

        self.security_service = SecurityService()

        self.report = self.security_service.analyze(
            path=path,
            process=process,
            connections=self.connections,
        )

        self.setWindowTitle(
            "Security Analysis"
        )

        self.setMinimumWidth(620)
        self.setMinimumHeight(540)

        self.setModal(True)

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            24,
            20,
            24,
            20,
        )

        main_layout.setSpacing(16)

        title = QLabel(
            "Security Analysis"
        )

        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)

        title.setFont(title_font)

        main_layout.addWidget(title)

        subtitle = QLabel(
            "Executable security and network information"
        )

        subtitle.setProperty(
            "secondary",
            True,
        )

        main_layout.addWidget(subtitle)

        separator = QFrameLine()

        main_layout.addWidget(separator)

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)
        scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        content = QWidget()

        details_layout = QGridLayout(
            content
        )

        details_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        details_layout.setHorizontalSpacing(20)
        details_layout.setVerticalSpacing(14)

        row = 0

        self.add_field(
            details_layout,
            row,
            "Process",
            self.report.process,
        )

        row += 1

        self.add_field(
            details_layout,
            row,
            "Publisher",
            self.report.publisher,
        )

        row += 1

        signature_label = self.create_value_label(
            self.report.digital_signature
        )

        signature_status = (
            self.report.signature_status.lower()
        )

        if signature_status == "valid":

            signature_label.setStyleSheet(
                """
                QLabel {
                    color: #4CAF50;
                    font-weight: 600;
                }
                """
            )

        elif signature_status in {
            "notsigned",
            "unsupported",
        }:

            signature_label.setStyleSheet(
                """
                QLabel {
                    color: #D9A441;
                    font-weight: 600;
                }
                """
            )

        else:

            signature_label.setStyleSheet(
                """
                QLabel {
                    color: #E05252;
                    font-weight: 600;
                }
                """
            )

        details_layout.addWidget(
            self.create_key_label(
                "Digital Signature"
            ),
            row,
            0,
        )

        details_layout.addWidget(
            signature_label,
            row,
            1,
        )

        row += 1

        self.add_field(
            details_layout,
            row,
            "SHA-256",
            self.report.sha256 or "Unavailable",
            selectable=True,
            monospace=True,
        )

        row += 1

        self.add_field(
            details_layout,
            row,
            "File Size",
            self.report.file_size_display,
        )

        row += 1

        self.add_field(
            details_layout,
            row,
            "Path",
            self.report.path,
            selectable=True,
            wrap=True,
        )

        row += 1

        self.add_field(
            details_layout,
            row,
            "Connections",
            str(self.report.connections),
        )

        row += 1

        countries = (
            ", ".join(
                self.report.remote_countries
            )
            if self.report.remote_countries
            else "None"
        )

        self.add_field(
            details_layout,
            row,
            "Remote Countries",
            countries,
        )

        if self.report.signer:

            row += 1

            self.add_field(
                details_layout,
                row,
                "Signer",
                self.report.signer,
                selectable=True,
                wrap=True,
            )

        scroll.setWidget(content)

        main_layout.addWidget(
            scroll,
            1,
        )

        button_layout = QHBoxLayout()

        button_layout.setSpacing(8)

        self.virus_total_button = QPushButton(
            "Open VirusTotal"
        )

        self.copy_hash_button = QPushButton(
            "Copy SHA256"
        )

        self.export_button = QPushButton(
            "Export Report"
        )

        self.close_button = QPushButton(
            "Close"
        )

        self.virus_total_button.clicked.connect(
            self.open_virustotal
        )

        self.copy_hash_button.clicked.connect(
            self.copy_sha256
        )

        self.export_button.clicked.connect(
            self.export_report
        )

        self.close_button.clicked.connect(
            self.reject
        )

        button_layout.addWidget(
            self.virus_total_button
        )

        button_layout.addWidget(
            self.copy_hash_button
        )

        button_layout.addWidget(
            self.export_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.close_button
        )

        main_layout.addLayout(
            button_layout
        )

    @staticmethod
    def create_key_label(
        text: str,
    ) -> QLabel:

        label = QLabel(text)

        label.setStyleSheet(
            """
            QLabel {
                font-weight: 600;
            }
            """
        )

        return label

    @staticmethod
    def create_value_label(
        text: str,
    ) -> QLabel:

        label = QLabel(text)

        label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        return label

    def add_field(
        self,
        layout: QGridLayout,
        row: int,
        key: str,
        value: str,
        selectable: bool = False,
        monospace: bool = False,
        wrap: bool = False,
    ):

        key_label = self.create_key_label(
            key
        )

        value_label = QLabel(value)

        value_label.setWordWrap(wrap)

        if selectable:

            value_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )

        if monospace:

            font = QFont(
                "Consolas"
            )

            value_label.setFont(font)

        layout.addWidget(
            key_label,
            row,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        layout.addWidget(
            value_label,
            row,
            1,
        )

    def open_virustotal(self):

        if not self.report.sha256:

            QMessageBox.warning(
                self,
                "SHA-256 Unavailable",
                "The SHA-256 hash could not be calculated, "
                "so VirusTotal cannot be queried.",
            )

            return

        BrowserService.virustotal(
            self.report.sha256
        )

    def copy_sha256(self):

        if not self.report.sha256:

            QMessageBox.warning(
                self,
                "SHA-256 Unavailable",
                "The SHA-256 hash could not be calculated.",
            )

            return

        clipboard = self.clipboard()

        clipboard.setText(
            self.report.sha256
        )

        self.copy_hash_button.setText(
            "Copied!"
        )

    def export_report(self):

        default_name = (
            f"{Path(self.report.path).stem}"
            "_security_report.json"
        )

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Security Report",
            default_name,
            "JSON Files (*.json)",
        )

        if not filename:
            return

        try:

            self.security_service.export_report(
                self.report,
                filename,
            )

        except OSError as exc:

            QMessageBox.critical(
                self,
                "Export Failed",
                f"Unable to export the report.\n\n{exc}",
            )

            return

        QMessageBox.information(
            self,
            "Report Exported",
            "Security report exported successfully.",
        )

    @staticmethod
    def clipboard():

        from PySide6.QtWidgets import QApplication

        return QApplication.clipboard()


class QFrameLine(QLabel):

    def __init__(self):

        super().__init__()

        self.setFixedHeight(1)

        self.setStyleSheet(
            """
            QLabel {
                background: #444444;
            }
            """
        )