from solve.triangle import solve_triangle


def test_right_triangle():
    solution, steps = solve_triangle({"a": 3.0, "b": 4.0, "right_at": "C"})
    assert round(solution["c"], 5) == 5.0
    assert any("Pythagoras" in step for step in steps)


def test_sas_triangle():
    solution, _ = solve_triangle({"a": 7.0, "b": 8.0, "C": 30.0})
    assert solution["c"] is not None
    assert solution["A"] is not None
    assert solution["B"] is not None


def test_insufficient_data():
    try:
        solve_triangle({"a": 5.0, "b": 6.0})
    except Exception as exc:
        assert "Insufficient" in str(exc)
    else:
        raise AssertionError("Should have raised")
