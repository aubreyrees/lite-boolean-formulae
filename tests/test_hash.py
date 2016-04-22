from lite_boolean_formulae import L


def test_literal_hash_same_for_the_same_literal():
    assert hash(L("x")) == hash(L("x"))


def test_literal_hash_different_for_the_different_literal():
    assert hash(L("x")) != hash(L("y"))


def test_formula_hash_same_for_the_same_formula():
    assert hash(L("x") & L("y")) == hash(L("y") & L("x"))


def test_formula_hash_different_for_the_different_formula():
    assert hash(L("a") & L("b")) != hash(L("y") & L("x"))
