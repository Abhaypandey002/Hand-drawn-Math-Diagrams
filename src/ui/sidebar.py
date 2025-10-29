"""Sidebar data model."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class SidebarItem:
    title: str
    subtitle: str = ""


@dataclass
class Sidebar:
    items: List[SidebarItem] = field(default_factory=list)

    def add_item(self, title: str, subtitle: str = "") -> None:
        self.items.append(SidebarItem(title, subtitle))

    def clear(self) -> None:
        self.items.clear()


__all__ = ["Sidebar", "SidebarItem"]
