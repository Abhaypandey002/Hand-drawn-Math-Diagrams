"""TrOCR fallback engine."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict

from core.bootstrap import ensure_model
from core.config import ModelConfig
from ocr.normalize import normalize_text

LOGGER = logging.getLogger(__name__)


class TrOCREngine:
    def __init__(self, cfg: ModelConfig) -> None:
        self.cfg = cfg
        self.model_path = Path(cfg.trocr_path) / "weights.pt"
        ensure_model(
            self.model_path,
            "https://example.com/trocr-weights.pt",
            "placeholder-checksum",
        )
        LOGGER.info("TrOCR engine initialized using %s", self.model_path)

    def infer(self, img_bgr) -> Dict[str, object]:  # pragma: no cover - heavy inference stub
        LOGGER.warning("TrOCR inference is stubbed in this lightweight build.")
        return {"latex": normalize_text(""), "confidence": 0.0}


__all__ = ["TrOCREngine"]
