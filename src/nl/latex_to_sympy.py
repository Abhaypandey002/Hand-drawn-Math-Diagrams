"""Convert LaTeX strings into lightweight symbolic objects."""
from __future__ import annotations

import re
from typing import Tuple

from .expressions import Equation, Expression, IntegralExpr


class LatexToSympyError(RuntimeError):
    pass


def _strip_latex_spacing(expr: str) -> str:
    expr = expr.replace("\\,", " ").replace("\\!", " ")
    expr = expr.replace("\\left", "").replace("\\right", "")
    expr = expr.replace("{", "(").replace("}", ")")
    expr = expr.replace("\\cdot", "*")
    expr = expr.replace("\\times", "*")
    return expr


def _normalize_product(expr: str) -> str:
    expr = re.sub(r"(?<=\d)\s+(?=[A-Za-z(])", "*", expr)
    expr = re.sub(r"(?<=[A-Za-z)])\s+(?=[A-Za-z(])", "*", expr)
    expr = re.sub(r"\s+", "", expr)
    expr = expr.replace("^", "**")
    return expr


def _normalize(expr: str) -> str:
    return _normalize_product(_strip_latex_spacing(expr))


def _extract_braced(text: str) -> Tuple[str, str]:
    if not text:
        return "", ""
    opening = text[0]
    if opening in "({[":
        closing_map = {"(": ")", "{": "}", "[": "]"}
        closing = closing_map[opening]
        depth = 0
        for idx, ch in enumerate(text):
            if ch == opening:
                depth += 1
            elif ch == closing:
                depth -= 1
                if depth == 0:
                    return text[1:idx], text[idx + 1 :]
        raise LatexToSympyError("Unbalanced delimiters in integral bounds")
    return text[0], text[1:]


def _parse_integral(latex: str):
    remainder = latex[len("\\int") :]
    remainder = remainder.lstrip()
    lower_expr = upper_expr = None
    if remainder.startswith("_"):
        remainder = remainder[1:]
        lower_expr, remainder = _extract_braced(remainder)
        if remainder.startswith("^"):
            remainder = remainder[1:]
            upper_expr, remainder = _extract_braced(remainder)
    remainder = remainder.lstrip()
    if remainder.startswith("^") and upper_expr is None:
        remainder = remainder[1:]
        upper_expr, remainder = _extract_braced(remainder)
    remainder = remainder.lstrip()
    parts = remainder.split("d", 1)
    if len(parts) != 2:
        raise LatexToSympyError("Integral missing differential")
    body, var_part = parts
    variable = var_part.strip()
    if variable.startswith("\\"):
        variable = variable[1:]
    variable = variable.strip()
    if not variable:
        raise LatexToSympyError("Could not determine integration variable")
    integrand = Expression.parse(_normalize(body))
    lower = Expression.parse(_normalize(lower_expr)) if lower_expr else None
    upper = Expression.parse(_normalize(upper_expr)) if upper_expr else None
    return IntegralExpr(integrand=integrand, variable=variable, lower=lower, upper=upper)


def latex_to_sympy(expr_latex: str):
    cleaned = expr_latex.strip()
    if not cleaned:
        raise LatexToSympyError("Empty LaTeX expression")
    if cleaned.startswith("\\int"):
        return _parse_integral(cleaned), "integral"
    if "=" in cleaned:
        left, right = cleaned.split("=", 1)
        left_expr = Expression.parse(_normalize(left))
        right_expr = Expression.parse(_normalize(right))
        return Equation(left=left_expr, right=right_expr), "equation"
    return Expression.parse(_normalize(cleaned)), "expr"


__all__ = ["latex_to_sympy", "LatexToSympyError"]
