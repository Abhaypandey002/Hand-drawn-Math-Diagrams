"""Answer board management."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .latex import LatexRenderResult, render_latex


@dataclass
class AnswerEntry:
    timestamp: datetime
    prompt: str
    latex: str
    steps: List[str]
    numeric: Optional[float] = None
    rendered: Optional[LatexRenderResult] = None


@dataclass
class AnswerBoard:
    entries: List[AnswerEntry] = field(default_factory=list)

    def add_entry(
        self,
        prompt: str,
        latex: str,
        steps: List[str],
        numeric: Optional[float] = None,
    ) -> AnswerEntry:
        rendered = render_latex(latex)
        entry = AnswerEntry(
            timestamp=datetime.utcnow(),
            prompt=prompt,
            latex=latex,
            steps=steps,
            numeric=numeric,
            rendered=rendered,
        )
        self.entries.append(entry)
        return entry

    def latest(self) -> Optional[AnswerEntry]:
        return self.entries[-1] if self.entries else None


__all__ = ["AnswerBoard", "AnswerEntry"]
