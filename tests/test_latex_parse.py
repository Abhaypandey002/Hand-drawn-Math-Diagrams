from nl.latex_to_sympy import latex_to_sympy
from nl.expressions import Equation, IntegralExpr


def test_parse_equation():
    expr, kind = latex_to_sympy(r"x^2 - 5 x + 6 = 0")
    assert isinstance(expr, Equation)
    assert kind == "equation"
    assert expr.left.text == "x**2-5*x+6"


def test_parse_integral():
    expr, kind = latex_to_sympy(r"\int_0^1 x^2 \, dx")
    assert isinstance(expr, IntegralExpr)
    assert kind == "integral"
    assert expr.variable == "x"


def test_parse_integral_with_braces():
    expr, kind = latex_to_sympy(r"\int_{0}^{1} x \, dx")
    assert isinstance(expr, IntegralExpr)
    assert kind == "integral"
    assert expr.variable == "x"
    assert expr.lower.text == "0"
    assert expr.upper.text == "1"
