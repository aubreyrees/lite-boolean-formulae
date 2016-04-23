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


def test_true_and_literal():
    assert (True & L("x")) == L("x") and (L("x") & True) == L("x")


def test_true_or_literal():
    assert ((True | L("x")) is True) and ((L("x") | True ) is True)


def test_false_and_literal():
    assert ((False & L("x")) is False) and ((L("x") & False) is False)


def test_false_or_literal():
    assert (False | L("x")) == L("x") and (L("x") | False) == L("x")


def test_true_and_formula():
    f = L("x") & L("y")
    assert (True & f) == f and (f & True) == f


def test_true_or_formula():
    f = L("x") | L("y")
    assert ((True | f) is True) and ((f | True) is True)


def test_false_and_formula():
    f = L("x") & L("y")
    assert ((False & f) is False) and ((f & False) is False)


def test_false_or_formula():
    f = L("x") | L("y")
    assert (False | f) == f and (f | False) == f


def test_substitute_true_into_disjuction():
    assert ((L("x") | L("y")).substitute("x", True)) is True


def test_substitute_false_into_conjunction():
    assert ((L("x") & L("y")).substitute("x", False) is False)


def test_literal_xored_with_self():
    assert ((L("x") ^ L("x")) is False)


def test_literal_xored_with_negated_self():
    assert ((L("x") ^ ~L("x")) is True)


def test_xor_is_associative():
    assert (L("x") ^ L("y")) == (L("y") ^ L("x"))


def test_literal_xored_with_false():
    assert ((L("x") ^ False) == L("x")) and ((False ^ L("x")) == L("x"))


def test_literal_xored_with_true():
    assert ((L("x") ^ True) == ~L("x")) and ((True ^ L("x")) == ~L("x"))
