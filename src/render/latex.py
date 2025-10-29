"""Utilities to render LaTeX snippets to raster images."""
from __future__ import annotations

import io
from dataclasses import dataclass
from typing import Tuple

import matplotlib.pyplot as plt


@dataclass
class LatexRenderResult:
    image_bytes: bytes
    dpi: int
    size_inches: Tuple[float, float]


def render_latex(latex: str, dpi: int = 160, font_size: int = 14) -> LatexRenderResult:
    plt.rc("text", usetex=False)
    fig = plt.figure(figsize=(4, 1), dpi=dpi)
    fig.patch.set_facecolor("white")
    ax = fig.add_subplot(111)
    ax.axis("off")
    ax.text(0.5, 0.5, f"$${latex}$$", fontsize=font_size, ha="center", va="center")
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=dpi, bbox_inches="tight", transparent=False)
    plt.close(fig)
    return LatexRenderResult(image_bytes=buffer.getvalue(), dpi=dpi, size_inches=fig.get_size_inches())


__all__ = ["render_latex", "LatexRenderResult"]
