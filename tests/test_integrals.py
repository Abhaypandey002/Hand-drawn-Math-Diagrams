from nl.expressions import Expression, IntegralExpr
from solve.calculus import solve_integral


def test_polynomial_integral():
    integral = IntegralExpr(Expression.parse("x**2"), "x", Expression.parse("0"), Expression.parse("1"))
    result, steps, numeric = solve_integral(integral)
    assert result == {3: 1 / 3}
    assert abs(numeric - (1 / 3)) < 1e-6
    assert any("integrated" in step.lower() for step in steps)


def test_indefinite_integral():
    integral = IntegralExpr(Expression.parse("x**2"), "x")
    result, steps, numeric = solve_integral(integral)
    assert result == {3: 1 / 3}
    assert numeric is None
