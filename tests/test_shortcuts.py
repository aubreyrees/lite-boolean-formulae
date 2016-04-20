from lite_boolean_formulae import L, and_, or_, is_boolean_formula


def test_and():
    assert (L("a") & L("b") & L("c") & L("d")) == and_("a", "b", "c", "d")


def test_or():
    assert (L("a") | L("b") | L("c") | L("d")) == or_("a", "b", "c", "d")


def test_is_boolean_formula_with_literal():
    assert is_boolean_formula(L("a")) is True


def test_is_boolean_formula_with_formula():
    assert is_boolean_formula(L("a") & L("b")) is True


def test_is_boolean_formula_with_non_boolean_obj():
    assert is_boolean_formula("XXX") is False
