from nl.expressions import Equation, Expression
from solve.algebra import solve_equation


def test_quadratic():
    eq = Equation(Expression.parse("x**2 - 5*x + 6"), Expression.parse("0"))
    solutions, steps = solve_equation(eq)
    assert set(round(sol, 5) for sol in solutions) == {2.0, 3.0}
    assert any("polynomial" in step.lower() for step in steps)


def test_linear_system():
    eq1 = Equation(Expression.parse("x + y"), Expression.parse("5"))
    eq2 = Equation(Expression.parse("2*x - y"), Expression.parse("1"))
    solution, steps = solve_equation([eq1, eq2])
    assert round(solution["x"], 5) == 2.0
    assert round(solution["y"], 5) == 3.0
    assert any("cramer" in step.lower() for step in steps)
