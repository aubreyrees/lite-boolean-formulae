from lite_boolean_formulae import L


def test_and_commutative():
    assert (L("x") & L("y") & L("z")) == (L("z") & L("y") & L("x"))


def test_or_commutative():
    assert (L("x") | L("y") | L("z")) == (L("z") | L("y") | L("x"))


def test_disjunction_over_conjunction():
    assert (L("x") | (L("y") & L("z"))) == ((L("x") | L("y")) & (L("x") | L("z")))


def test_conjunction_over_disjunction():
    assert (L("x") & (L("y") | L("z"))) == ((L("x") & L("y")) | (L("x") & L("z")))


def test_de_morgan_negation_of_conjunction():
    assert (~(L("x") & L("y"))) == ((~L("x")) | (~L("y")))


def test_de_morgan_negation_of_disjunction():
    assert (~(L("x") | L("y"))) == ((~L("x")) & (~L("y")))


def double_negation():
    assert (~(~L("x"))) == L("x")


def test_substitute_and():
    L("x").substitute("x", L("y") & (L("z")) == L("y") & L("z"))


def test_substitute_or():
    L("x").substitute("x", L("y") | (L("z")) == L("y") | L("z"))


def test_complex_subsistute():
    pass
