"""Pix2Tex OCR engine wrapper."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

from core.bootstrap import ensure_model
from core.config import ModelConfig
from ocr.normalize import normalize_text

LOGGER = logging.getLogger(__name__)


class Pix2TexEngine:
    def __init__(self, cfg: ModelConfig) -> None:
        self.cfg = cfg
        self.model_path = Path(cfg.pix2tex_path) / "weights.pt"
        ensure_model(
            self.model_path,
            "https://example.com/pix2tex-weights.pt",
            "placeholder-checksum",
        )
        LOGGER.info("Pix2Tex engine initialized using %s", self.model_path)

    def infer(self, img_bgr) -> Dict[str, object]:  # pragma: no cover - heavy inference stub
        LOGGER.warning("Pix2Tex inference is stubbed in this lightweight build.")
        return {"latex": normalize_text(""), "confidence": 0.0}


__all__ = ["Pix2TexEngine"]
