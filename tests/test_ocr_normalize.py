from ocr.normalize import normalize_text


def test_minus_variants():
    assert normalize_text("1 − 2") == "1 - 2"


def test_angle_and_degree():
    assert normalize_text("∠C = 30°") == "\\angleC = 30^\\circ"


def test_l_vs_one():
    assert normalize_text("l + O") == "1 + 0"
