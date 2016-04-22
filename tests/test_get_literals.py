from lite_boolean_formulae import L


def test_get_literals_from_literal():
    assert L("x").get_literals() == frozenset(("x",))


def test_get_literals_from_formula():
    assert ((L("x")  & L("y")) | L("z")).get_literals() == frozenset(("x", "y", "z"))
