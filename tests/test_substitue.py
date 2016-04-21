from lite_boolean_formulae import L


def test_substitute_and():
    L("x").substitute("x", L("y") & L("z")) == (L("y") & L("z"))


def test_negated_substitute_and():
    (~L("x")).substitute("x", L("y") & L("z")) == ((~L("y")) | (~L("z")))


def test_substitute_or():
    L("x").substitute("x", L("y") | L("z")) == (L("y") | L("z"))


def test_negated_substitute_or():
    (~L("x")).substitute("x", L("y") | L("z")) == ((~L("y")) & (~L("z")))


def test_formula_substitue_conjunction_into_conjunctiom():
    assert (L("a") & L("b")).substitute("a", L("c") & L("d")) == (L("b") & L("d") & L("c"))


def test_formula_substitue_conjuntion_into_disjunction():
    assert (L("a") | L("b")).substitute("a", L("c") & L("d")) == (L("b") | (L("d") & L("c")))


def test_formula_substitue_disjuntion_into_disjunction():
    assert (L("a") | L("b")).substitute("a", L("c") | L("d")) == (L("b") | L("d") | L("c"))


def test_formula_substitue_disjuntion_into_conjunction():
    assert (L("a") & L("b")).substitute("a", L("c") | L("d")) == (L("b") & (L("d") | L("c")))
