"""Structured logging setup."""
from __future__ import annotations

import logging
import os
from logging import Handler
from pathlib import Path
from typing import Optional

from rich.logging import RichHandler

from .config import CONFIG_DIR, LoggingConfig


def build_handlers(config: LoggingConfig) -> list[Handler]:
    handlers: list[Handler] = [
        RichHandler(
            rich_tracebacks=True,
            tracebacks_show_locals=False,
            markup=True,
            show_level=True,
            show_time=True,
        )
    ]
    if config.to_file:
        log_dir = CONFIG_DIR / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "inkmath.log", encoding="utf-8")
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    return handlers


def setup_logging(config: LoggingConfig) -> None:
    handlers = build_handlers(config)
    logging.basicConfig(
        level=getattr(logging, config.level.upper(), logging.INFO),
        handlers=handlers,
        force=True,
    )
    logging.getLogger("transformers").setLevel(logging.WARNING)
    logging.getLogger("torch").setLevel(logging.WARNING)


__all__ = ["setup_logging"]
