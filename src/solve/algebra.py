"""Algebraic solvers built on lightweight symbolic expressions."""
from __future__ import annotations

import ast
import math
from typing import Dict, List, Sequence

from nl.expressions import Equation
from .polynomials import from_ast


class AlgebraError(RuntimeError):
    pass


def _poly_difference(eq: Equation, variable: str) -> Dict[int, float]:
    diff = eq.as_difference()
    return from_ast(diff.node, variable)


def _poly_to_coeff_list(poly: Dict[int, float]) -> List[float]:
    degree = max(poly)
    coeffs = [0.0] * (degree + 1)
    for power, coeff in poly.items():
        coeffs[power] = coeff
    return coeffs


def _solve_polynomial(coeffs: List[float]):
    degree = len(coeffs) - 1
    if degree == 1:
        b, a = coeffs
        if a == 0:
            raise AlgebraError("Degenerate linear equation")
        return [-(b) / a]
    if degree == 2:
        c, b, a = coeffs
        if a == 0:
            return _solve_polynomial([c, b])
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            real = -b / (2 * a)
            imag = math.sqrt(-discriminant) / (2 * a)
            return [complex(real, imag), complex(real, -imag)]
        sqrt_disc = math.sqrt(discriminant)
        return [(-b + sqrt_disc) / (2 * a), (-b - sqrt_disc) / (2 * a)]
    raise AlgebraError("Polynomial degree not supported")


def _solve_single_equation(eq: Equation):
    if not eq.variables:
        raise AlgebraError("Equation has no variables")
    variable = sorted(eq.variables)[0]
    poly = _poly_difference(eq, variable)
    coeffs = _poly_to_coeff_list(poly)
    solutions = _solve_polynomial(coeffs)
    steps = [f"Selected variable {variable}", "Converted to polynomial", "Solved using analytical formula"]
    return solutions, steps


def _linear_terms(node: ast.AST) -> Dict[str, float]:
    if isinstance(node, ast.Constant):
        return {"__const__": float(node.value)}
    if isinstance(node, ast.Name):
        return {node.id: 1.0}
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        terms = _linear_terms(node.operand)
        return {k: -v for k, v in terms.items()}
    if isinstance(node, ast.BinOp):
        left = _linear_terms(node.left)
        right = _linear_terms(node.right)
        if isinstance(node.op, ast.Add):
            return {k: left.get(k, 0.0) + right.get(k, 0.0) for k in set(left) | set(right)}
        if isinstance(node.op, ast.Sub):
            return {k: left.get(k, 0.0) - right.get(k, 0.0) for k in set(left) | set(right)}
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.Constant):
                scale = float(node.left.value)
                terms = _linear_terms(node.right)
                return {k: scale * v for k, v in terms.items()}
            if isinstance(node.right, ast.Constant):
                scale = float(node.right.value)
                terms = _linear_terms(node.left)
                return {k: scale * v for k, v in terms.items()}
    raise AlgebraError("Equation is not linear")


def _solve_system(equations: Sequence[Equation]):
    vars_sorted = sorted({var for eq in equations for var in eq.variables})
    if not vars_sorted:
        raise AlgebraError("System has no variables")
    if len(vars_sorted) != len(equations):
        raise AlgebraError("System must have same number of equations and variables")
    if len(vars_sorted) == 1:
        return _solve_single_equation(equations[0])
    if len(vars_sorted) == 2 and len(equations) == 2:
        rows = []
        consts = []
        for eq in equations:
            diff = eq.as_difference()
            terms = _linear_terms(diff.node)
            row = [terms.get(var, 0.0) for var in vars_sorted]
            const = -terms.get("__const__", 0.0)
            rows.append(row)
            consts.append(const)
        a11, a12 = rows[0]
        a21, a22 = rows[1]
        b1, b2 = consts
        det = a11 * a22 - a12 * a21
        if det == 0:
            raise AlgebraError("System determinant is zero")
        x = (b1 * a22 - a12 * b2) / det
        y = (a11 * b2 - b1 * a21) / det
        solution = {vars_sorted[0]: x, vars_sorted[1]: y}
        steps = ["Constructed linear system", "Solved using Cramer's rule"]
        return solution, steps
    raise AlgebraError("Only 2x2 linear systems are supported")


def solve_equation(eq):
    if isinstance(eq, (list, tuple)):
        equations = [e for e in eq]
        return _solve_system(equations)
    if not isinstance(eq, Equation):
        raise AlgebraError("Expected Equation instance")
    return _solve_single_equation(eq)


__all__ = ["solve_equation", "AlgebraError"]
