"""Integral solving helpers for lightweight symbolic expressions."""
from __future__ import annotations

import ast
from typing import List, Optional

from nl.expressions import IntegralExpr
from .polynomials import from_ast


class CalculusError(RuntimeError):
    pass


def _poly_integral(poly: dict[int, float]) -> dict[int, float]:
    result: dict[int, float] = {}
    for power, coeff in poly.items():
        result[power + 1] = coeff / (power + 1)
    return result


def _evaluate_polynomial(poly: dict[int, float], value: float) -> float:
    total = 0.0
    for power, coeff in poly.items():
        total += coeff * (value ** power)
    return total


def _eval_constant(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_constant(node.operand)
    if isinstance(node, ast.BinOp):
        left = _eval_constant(node.left)
        right = _eval_constant(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
    raise CalculusError("Integral bounds must be numeric constants")


def solve_integral(obj: IntegralExpr):
    if not isinstance(obj, IntegralExpr):
        raise CalculusError("Expected IntegralExpr")
    poly = from_ast(obj.integrand.node, obj.variable)
    integrated = _poly_integral(poly)
    steps: List[str] = ["Parsed integral", "Integrated polynomial analytically"]
    numeric: Optional[float] = None
    if obj.lower is not None and obj.upper is not None:
        lower_val = _eval_constant(obj.lower.node)
        upper_val = _eval_constant(obj.upper.node)
        numeric = _evaluate_polynomial(integrated, upper_val) - _evaluate_polynomial(integrated, lower_val)
        steps.append("Evaluated definite integral")
    return integrated, steps, numeric


__all__ = ["solve_integral", "CalculusError"]
