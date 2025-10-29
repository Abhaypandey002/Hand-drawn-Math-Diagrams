"""Canvas layer manager."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import numpy as np

from .strokes import Stroke


@dataclass
class InkCanvas:
    width: int
    height: int
    strokes: List[Stroke] = field(default_factory=list)

    def new_stroke(self, color=(0, 0, 0), thickness: int = 3) -> Stroke:
        stroke = Stroke(color=color, thickness=thickness)
        self.strokes.append(stroke)
        return stroke

    def to_image(self) -> np.ndarray:
        img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        for stroke in self.strokes:
            points = stroke.to_array()
            if len(points) > 1:
                for start, end in zip(points, points[1:]):
                    start_t = tuple(int(v) for v in start)
                    end_t = tuple(int(v) for v in end)
                    import cv2

                    cv2.line(img, start_t, end_t, stroke.color, stroke.thickness, lineType=cv2.LINE_AA)
        return img

    def clear(self) -> None:
        self.strokes.clear()


__all__ = ["InkCanvas"]
