"""Hotkey registry."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict


@dataclass
class Hotkey:
    key: str
    description: str
    action: Callable[[], None]


class HotkeyManager:
    def __init__(self) -> None:
        self._hotkeys: Dict[str, Hotkey] = {}

    def register(self, key: str, description: str, action: Callable[[], None]) -> None:
        self._hotkeys[key.lower()] = Hotkey(key.lower(), description, action)

    def trigger(self, key: str) -> bool:
        hk = self._hotkeys.get(key.lower())
        if hk:
            hk.action()
            return True
        return False

    def describe(self) -> Dict[str, str]:
        return {hk.key: hk.description for hk in self._hotkeys.values()}


__all__ = ["HotkeyManager", "Hotkey"]
