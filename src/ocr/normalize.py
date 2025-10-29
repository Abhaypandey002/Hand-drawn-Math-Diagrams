"""Normalization utilities for OCR outputs."""
from __future__ import annotations

import re

COMMON_REPLACEMENTS = {
    "−": "-",
    "–": "-",
    "—": "-",
    "÷": "/",
    "×": "x",
    "∠": "\\angle ",
    "°": "^\\circ",
}


def _fix_misread_digits(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return "1" if token.lower() == "l" else token

    return re.sub(r"\b[lL]\b", replace, text)


def normalize_text(text: str) -> str:
    result = text
    for src, dst in COMMON_REPLACEMENTS.items():
        result = result.replace(src, dst)
    result = re.sub(r"(?<=\\angle)\s+", "", result)
    result = _fix_misread_digits(result)
    result = result.replace("O", "0")
    result = re.sub(r"\\?mathrm\{dx\}", " dx", result)
    result = re.sub(r"\s+", " ", result)
    return result.strip()


__all__ = ["normalize_text"]
