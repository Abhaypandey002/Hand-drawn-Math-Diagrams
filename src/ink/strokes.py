"""Stroke data structures."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np


@dataclass
class Stroke:
    points: List[Tuple[int, int]] = field(default_factory=list)
    color: Tuple[int, int, int] = (0, 0, 0)
    thickness: int = 3

    def add_point(self, point: Tuple[int, int]) -> None:
        self.points.append(point)

    def to_array(self) -> np.ndarray:
        return np.array(self.points, dtype=np.int32)


__all__ = ["Stroke"]
