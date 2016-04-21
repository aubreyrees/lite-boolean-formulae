from lite_boolean_formulae import L


def test_literal_contains():
    assert ("x" in L("x"))


def test_conjunction_formula_contains():
    assert ("x" in (L("x") & L("y")))


def test_disjunction_formula_contains():
    assert ("x" in (L("x") | L("y")))


def test_disjunction_formula_does_not_contain():
    assert not ("x" in (L("a") | L("b")))


def test_conjunction_formula_does_not_contain():
    assert not ("x" in (L("a") & L("b")))
