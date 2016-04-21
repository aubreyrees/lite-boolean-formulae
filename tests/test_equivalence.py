from lite_boolean_formulae import (
    L,
    Tautology,
    Contradiction,
    is_contradiction,
    is_tautology
)


def test_reflexive():
    assert L("x") == L("x")


def test_conjunction_with_negation():
    assert is_contradiction(L("x") & (~L("x")))


def test_disjunction_with_negation():
    assert is_tautology(L("x") | (~L("x")))


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


def test_negate_tautology():
    assert is_contradiction(~Tautology)


def test_negate_contradiction():
    assert is_tautology(~Contradiction)


def test_tautology_with_and():
    assert (Tautology & L("x")) == L("x") and (L("x") & Tautology) == L("x")


def test_tautology_with_or():
    assert is_tautology(Tautology | L("x")) and is_tautology(L("x") | Tautology )


def test_contradiction_with_and():
    assert is_contradiction(Contradiction & L("x")) and is_contradiction(L("x") & Contradiction )


def test_contradiction_with_or():
    assert (Contradiction | L("x")) == L("x") and (L("x") | Contradiction) == L("x")
