"""Triangle solver implementation."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional


class TriangleError(RuntimeError):
    pass


def _deg(x: float) -> float:
    return math.degrees(x)


def _rad(x: float) -> float:
    return math.radians(x)


def _law_of_cosines_for_angle(a: float, b: float, c: float) -> float:
    return _deg(math.acos((a**2 + b**2 - c**2) / (2 * a * b)))


def _law_of_cosines_for_side(a: float, b: float, gamma: float) -> float:
    rad = _rad(gamma)
    return math.sqrt(a**2 + b**2 - 2 * a * b * math.cos(rad))


def _law_of_sines_for_angle(a: float, A: float, b: float) -> float:
    if a is None or b is None:
        raise TriangleError("Missing side length for law of sines computation")
    if a <= 0:
        raise TriangleError("Side lengths must be positive for law of sines")
    ratio = math.sin(_rad(A)) * b / a
    if not math.isfinite(ratio):
        raise TriangleError("Invalid ratio computed for law of sines")
    epsilon = 1e-7
    if ratio > 1 + epsilon or ratio < -1 - epsilon:
        raise TriangleError("Inconsistent measurements for law of sines")
    ratio = max(-1.0, min(1.0, ratio))
    return _deg(math.asin(ratio))


def _heron(a: float, b: float, c: float) -> float:
    s = (a + b + c) / 2
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def solve_triangle(meas: Dict[str, Optional[float]]):
    a = meas.get("a")
    b = meas.get("b")
    c = meas.get("c")
    A = meas.get("A")
    B = meas.get("B")
    C = meas.get("C")
    right_at = meas.get("right_at")
    steps: List[str] = []

    def known_angles() -> Dict[str, float]:
        return {k: v for k, v in {"A": A, "B": B, "C": C}.items() if v is not None}

    def known_sides() -> Dict[str, float]:
        return {k: v for k, v in {"a": a, "b": b, "c": c}.items() if v is not None}

    if right_at:
        steps.append(f"Detected right angle at {right_at}")
        if right_at == "C" and a is not None and b is not None:
            c = math.hypot(a, b)
            steps.append("Used Pythagoras to compute c")
            C = 90.0
        elif right_at == "A" and b is not None and c is not None:
            a = math.hypot(b, c)
            steps.append("Used Pythagoras to compute a")
            A = 90.0
        elif right_at == "B" and a is not None and c is not None:
            b = math.hypot(a, c)
            steps.append("Used Pythagoras to compute b")
            B = 90.0

    # Fill with Law of Cosines if two sides and included angle known
    if sum(v is not None for v in (a, b, c)) == 2 and len(known_angles()) >= 1:
        if A is not None and b is not None and c is not None and a is None:
            a = _law_of_cosines_for_side(b, c, A)
            steps.append("Law of Cosines to compute side a")
        if B is not None and a is not None and c is not None and b is None:
            b = _law_of_cosines_for_side(a, c, B)
            steps.append("Law of Cosines to compute side b")
        if C is not None and a is not None and b is not None and c is None:
            c = _law_of_cosines_for_side(a, b, C)
            steps.append("Law of Cosines to compute side c")

    # Use law of cosines for angles when three sides known
    if all(val is not None for val in (a, b, c)):
        if A is None:
            A = _law_of_cosines_for_angle(b, c, a)
            steps.append("Law of Cosines to compute angle A")
        if B is None:
            B = _law_of_cosines_for_angle(a, c, b)
            steps.append("Law of Cosines to compute angle B")
        if C is None:
            C = 180.0 - A - B
            steps.append("Used angle sum to compute C")

    # Use law of sines for remaining values
    if len(known_angles()) >= 2 and all(side is not None for side in (a, b, c)):
        pass
    else:
        # Use law of sines to fill missing pieces when possible
        if A is not None and a is not None:
            if B is None and b is not None:
                B = _law_of_sines_for_angle(a, A, b)
                steps.append("Law of Sines to compute B")
            if C is None and c is not None:
                C = _law_of_sines_for_angle(a, A, c)
                steps.append("Law of Sines to compute C")
        if B is not None and b is not None:
            if A is None and a is not None:
                A = _law_of_sines_for_angle(b, B, a)
                steps.append("Law of Sines to compute A")
            if C is None and c is not None:
                C = _law_of_sines_for_angle(b, B, c)
                steps.append("Law of Sines to compute C")
        if C is not None and c is not None:
            if A is None and a is not None:
                A = _law_of_sines_for_angle(c, C, a)
                steps.append("Law of Sines to compute A")
            if B is None and b is not None:
                B = _law_of_sines_for_angle(c, C, b)
                steps.append("Law of Sines to compute B")

    if sum(v is not None for v in (A, B, C)) == 2:
        missing = 180.0 - sum(v for v in (A, B, C) if v is not None)
        if A is None:
            A = missing
            steps.append("Angle sum to compute A")
        elif B is None:
            B = missing
            steps.append("Angle sum to compute B")
        elif C is None:
            C = missing
            steps.append("Angle sum to compute C")

    if not all(val is not None for val in (a, b, c, A, B, C)):
        raise TriangleError("Insufficient information to solve triangle")

    perimeter = a + b + c
    area = _heron(a, b, c)
    steps.append("Computed perimeter and area via Heron's formula")

    solution = {
        "a": a,
        "b": b,
        "c": c,
        "A": A,
        "B": B,
        "C": C,
        "perimeter": perimeter,
        "area": area,
    }
    return solution, steps


__all__ = ["solve_triangle", "TriangleError"]
