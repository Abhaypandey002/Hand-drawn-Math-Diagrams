"""Model bootstrap utilities."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Iterable, Tuple

from rich.console import Console

console = Console()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_model(path: Path, url: str, checksum: str) -> None:
    """Ensure that a model file exists, downloading if needed.

    The actual download is deferred to scripts/fetch_models.py to keep runtime fast and
    avoid network operations during automated tests. If the model is missing this function
    prints a helpful message so the user can fetch the assets manually.
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        current = _sha256(path)
        if current != checksum:
            console.print(f"[yellow]Checksum mismatch for {path}. Expected {checksum}, got {current}.")
            console.print("Please re-run scripts/fetch_models.py to refresh the weights.")
        return

    console.print(
        f"[cyan]Model file {path.name} not found. Run `python scripts/fetch_models.py --url {url} --out {path}`"
        " to download the weights before first OCR run.",
    )


def verify_models(models: Iterable[Tuple[Path, str, str]]) -> None:
    for path, url, checksum in models:
        ensure_model(path, url, checksum)


__all__ = ["ensure_model", "verify_models"]
