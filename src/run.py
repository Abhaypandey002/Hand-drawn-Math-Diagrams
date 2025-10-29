"""InkMath entry point."""
from __future__ import annotations

import logging
import time
from pathlib import Path

import cv2
import numpy as np

from core.bootstrap import verify_models
from core.config import CONFIG_DIR, AppConfig, load_config, parse_cli
from core.logging_setup import setup_logging
from render.board import AnswerBoard

LOGGER = logging.getLogger(__name__)


PIX2TEX_INFO = (
    Path(CONFIG_DIR / "models" / "pix2tex" / "weights.pt"),
    "https://example.com/pix2tex-weights.pt",
    "placeholder-checksum",
)
TROCR_INFO = (
    Path(CONFIG_DIR / "models" / "trocr" / "weights.pt"),
    "https://example.com/trocr-weights.pt",
    "placeholder-checksum",
)


class SimpleCanvas:
    """A very small OpenCV-based canvas suitable for early development."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.size = (config.canvas.height, config.canvas.width, 3)
        self.canvas = np.ones(self.size, dtype=np.uint8) * 255
        self.window_name = "InkMath Canvas"
        self.drawing = False
        self.last_point: tuple[int, int] | None = None
        self.brush_color = (0, 0, 0)
        self.brush_size = 4
        self.answer_board = AnswerBoard()

    def _draw_line(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        cv2.line(self.canvas, start, end, self.brush_color, self.brush_size, lineType=cv2.LINE_AA)

    def on_mouse(self, event: int, x: int, y: int, *_args) -> None:  # pragma: no cover - UI callback
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.last_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            if self.last_point is not None:
                self._draw_line(self.last_point, (x, y))
            self.last_point = (x, y)
        elif event in (cv2.EVENT_LBUTTONUP, cv2.EVENT_MOUSEMOVE) and not self.drawing:
            self.last_point = None
        if event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.last_point = None

    def reset(self) -> None:
        self.canvas[:] = 255

    def run(self) -> None:  # pragma: no cover - UI loop
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.config.canvas.width, self.config.canvas.height)
        cv2.setMouseCallback(self.window_name, self.on_mouse)
        LOGGER.info("InkMath canvas ready. Press 'c' to clear, 'q' to quit.")
        while True:
            cv2.imshow(self.window_name, self.canvas)
            key = cv2.waitKey(16) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                self.reset()
        cv2.destroyAllWindows()


def bootstrap_models(config: AppConfig) -> None:
    models = [PIX2TEX_INFO]
    if config.ocr.engine == "trocr":
        models.append(TROCR_INFO)
    verify_models(models)


def main() -> None:
    args = parse_cli()
    config = load_config(args)
    setup_logging(config.logging)
    LOGGER.info("Starting InkMath with engine=%s on %s", config.ocr.engine, config.models.device)
    bootstrap_models(config)
    canvas = SimpleCanvas(config)
    LOGGER.info("Launching UI loop")
    canvas.run()


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
