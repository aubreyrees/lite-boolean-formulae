from lite_boolean_formulae import L


def test_reflexive():
    assert L("x") == L("x")


def test_conjunction_with_negation():
    assert ((L("x") & (~L("x"))) is False)


def test_disjunction_with_negation():
    assert ((L("x") | (~L("x"))) is True)


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


def test_tautology_with_and():
    assert (True & L("x")) == L("x") and (L("x") & True) == L("x")


def test_tautology_with_or():
    assert ((True | L("x")) is True) and ((L("x") | True ) is True)


def test_contradiction_with_and():
    assert ((False & L("x")) is False) and ((L("x") & False) is False)


def test_contradiction_with_or():
    assert (False | L("x")) == L("x") and (L("x") | False) == L("x")


def test_tautology_with_and_formula():
    f = L("x") & L("y")
    assert (True & f) == f and (f & True) == f


def test_tautology_with_or_formula():
    f = L("x") | L("y")
    assert ((True | f) is True) and ((f | True) is True)


def test_contradiction_with_and_formula():
    f = L("x") & L("y")
    assert ((False & f) is False) and ((f & False) is False)


def test_contradiction_with_or():
    f = L("x") | L("y")
    assert (False | f) == f and (f | False) == f


def test_substitute_tautology_into_disjuction():
    assert ((L("x") | L("y")).substitute("x", True)) is True


def test_substitute_contradiction_into_conjunction():
    assert ((L("x") & L("y")).substitute("x", False) is False)
