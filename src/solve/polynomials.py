"""Shared helpers for polynomial manipulation."""
from __future__ import annotations

import ast
from typing import Dict


class PolynomialError(RuntimeError):
    pass


def combine(a: Dict[int, float], b: Dict[int, float]) -> Dict[int, float]:
    result = a.copy()
    for power, coeff in b.items():
        result[power] = result.get(power, 0.0) + coeff
    return result


def multiply(a: Dict[int, float], b: Dict[int, float]) -> Dict[int, float]:
    result: Dict[int, float] = {}
    for p1, c1 in a.items():
        for p2, c2 in b.items():
            power = p1 + p2
            result[power] = result.get(power, 0.0) + c1 * c2
    return result


def from_ast(node: ast.AST, variable: str) -> Dict[int, float]:
    from .algebra import AlgebraError  # Avoid circular import at module level

    if isinstance(node, ast.Constant):
        return {0: float(node.value)}
    if isinstance(node, ast.Name):
        if node.id != variable:
            raise AlgebraError(f"Unexpected variable {node.id}")
        return {1: 1.0}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        poly = from_ast(node.operand, variable)
        return {power: -coeff for power, coeff in poly.items()}
    if isinstance(node, ast.BinOp):
        if isinstance(node.op, (ast.Add, ast.Sub)):
            left = from_ast(node.left, variable)
            right = from_ast(node.right, variable)
            if isinstance(node.op, ast.Sub):
                right = {power: -coeff for power, coeff in right.items()}
            return combine(left, right)
        if isinstance(node.op, ast.Mult):
            left = from_ast(node.left, variable)
            right = from_ast(node.right, variable)
            return multiply(left, right)
        if isinstance(node.op, ast.Pow):
            base = from_ast(node.left, variable)
            if len(base) != 1 or 1 not in base:
                raise AlgebraError("Power only supported on pure variable")
            if not isinstance(node.right, ast.Constant):
                raise AlgebraError("Exponent must be constant")
            exponent = int(node.right.value)
            result = {0: 1.0}
            for _ in range(exponent):
                result = multiply(result, base)
            return result
    raise AlgebraError(f"Unsupported expression: {ast.dump(node)}")
