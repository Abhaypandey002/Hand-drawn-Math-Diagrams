"""Utility script to download OCR models."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen

CHUNK_SIZE = 1024 * 1024


def download(url: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(url) as response, out.open("wb") as fh:
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break
            fh.write(chunk)


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch OCR model weights")
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    path = Path(args.out).expanduser()
    download(args.url, path)
    print(f"Downloaded to {path}. sha256={checksum(path)}")


if __name__ == "__main__":  # pragma: no cover
    main()
