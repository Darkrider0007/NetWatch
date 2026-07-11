"""
Filter State

Stores all currently selected filters.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class FilterState:

    search: str = ""

    protocol: str = "ALL"

    country: str = "ALL"

    publisher: str = "ALL"

    established_only: bool = False

    show_system: bool = False