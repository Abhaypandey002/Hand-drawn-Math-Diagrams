"""Lightweight symbolic expression helpers."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Optional, Set

ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    ast.Name,
    ast.Constant,
    ast.Load,
)


def _assert_safe(node: ast.AST) -> None:
    for child in ast.walk(node):
        if not isinstance(child, ALLOWED_NODES):
            raise ValueError(f"Unsupported syntax in expression: {ast.dump(child)}")


def _gather_symbols(node: ast.AST) -> Set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


@dataclass
class Expression:
    text: str
    node: ast.AST

    @classmethod
    def parse(cls, text: str) -> "Expression":
        parsed = ast.parse(text, mode="eval")
        _assert_safe(parsed)
        return cls(text=text, node=parsed.body)

    @property
    def variables(self) -> Set[str]:
        return _gather_symbols(self.node)


@dataclass
class Equation:
    left: Expression
    right: Expression

    @property
    def variables(self) -> Set[str]:
        return self.left.variables | self.right.variables

    def as_difference(self) -> Expression:
        return Expression.parse(f"({self.left.text})-({self.right.text})")


@dataclass
class IntegralExpr:
    integrand: Expression
    variable: str
    lower: Optional[Expression] = None
    upper: Optional[Expression] = None


__all__ = ["Expression", "Equation", "IntegralExpr"]
