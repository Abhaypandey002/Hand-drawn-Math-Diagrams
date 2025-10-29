"""Shape heuristics for ink strokes."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np

from .strokes import Stroke


@dataclass
class DetectedTriangle:
    vertices: List[Tuple[int, int]]


class TriangleDetector:
    def __init__(self, tolerance: float = 0.02) -> None:
        self.tolerance = tolerance

    def detect(self, strokes: List[Stroke]) -> List[DetectedTriangle]:
        mask = np.zeros((1024, 1024), dtype=np.uint8)
        for stroke in strokes:
            pts = stroke.to_array()
            if len(pts) > 1:
                cv2.polylines(mask, [pts], False, 255, stroke.thickness)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        triangles: List[DetectedTriangle] = []
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, self.tolerance * peri, True)
            if len(approx) == 3:
                vertices = [(int(pt[0][0]), int(pt[0][1])) for pt in approx]
                triangles.append(DetectedTriangle(vertices=vertices))
        return triangles


__all__ = ["TriangleDetector", "DetectedTriangle"]
