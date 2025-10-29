"""Configuration management for InkMath."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field

CONFIG_DIR = Path(os.path.expanduser("~/.inkmath"))
CONFIG_PATH = CONFIG_DIR / "config.yaml"


class CanvasConfig(BaseModel):
    width: int = 1280
    height: int = 720
    bg_color: str = "white"
    smoothing: bool = True


class OcrConfig(BaseModel):
    engine: str = "pix2tex"
    debounce_ms: int = 600
    min_confidence: float = 0.4


class ModelConfig(BaseModel):
    device: str = "cpu"
    pix2tex_path: str = Field(default_factory=lambda: str(CONFIG_DIR / "models" / "pix2tex"))
    trocr_path: str = Field(default_factory=lambda: str(CONFIG_DIR / "models" / "trocr"))


class SolveConfig(BaseModel):
    timeout_ms_symbolic: int = 800
    numeric_fallback: bool = True


class RenderConfig(BaseModel):
    dpi: int = 160
    font_size: int = 14
    theme: str = "dark"


class LoggingConfig(BaseModel):
    level: str = "INFO"
    to_file: bool = True


class AppConfig(BaseModel):
    canvas: CanvasConfig = Field(default_factory=CanvasConfig)
    ocr: OcrConfig = Field(default_factory=OcrConfig)
    models: ModelConfig = Field(default_factory=ModelConfig)
    solve: SolveConfig = Field(default_factory=SolveConfig)
    render: RenderConfig = Field(default_factory=RenderConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    def merge_overrides(self, overrides: Dict[str, Any]) -> "AppConfig":
        data = self.dict()
        for dotted_key, value in overrides.items():
            section, key = dotted_key.split(".", 1)
            if section in data and isinstance(data[section], dict):
                data[section][key] = value
        return AppConfig.parse_obj(data)


DEFAULT_CONFIG = AppConfig()


def ensure_default_config() -> AppConfig:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r", encoding="utf-8") as fh:
            payload = yaml.safe_load(fh) or {}
        config = AppConfig.parse_obj(payload)
    else:
        config = DEFAULT_CONFIG
        with CONFIG_PATH.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(config.dict(), fh, sort_keys=False)
    return config


def load_config(args: Optional[argparse.Namespace] = None) -> AppConfig:
    config = ensure_default_config()
    overrides: Dict[str, Any] = {}
    if args is not None:
        if getattr(args, "engine", None):
            overrides["ocr.engine"] = args.engine
        if getattr(args, "device", None):
            overrides["models.device"] = args.device
        if getattr(args, "theme", None):
            overrides["render.theme"] = args.theme
    if overrides:
        config = config.merge_overrides(overrides)
    return config


def write_config(config: AppConfig) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(config.dict(), fh, sort_keys=False)


def parse_cli(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="InkMath whiteboard")
    parser.add_argument("--engine", choices=["pix2tex", "trocr"], help="OCR engine override")
    parser.add_argument("--device", choices=["cpu", "cuda"], help="Torch device override")
    parser.add_argument("--theme", choices=["light", "dark"], help="UI theme override")
    return parser.parse_args(argv)
