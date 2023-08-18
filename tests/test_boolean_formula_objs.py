import re
from lite_boolean_formulae import L


def _test_str(cls, r):
    assert re.match(f"^{r}$", str(cls))


def _test_repr(obj):
    assert isinstance(repr(obj), str)



def test_repr_formula():
    _test_repr(L("x") & L("y"))


def test_repr_literal():
    _test_repr(L("x"))


def test_repr_negated_literal():
    _test_repr(~L("x"))


def test_literal_str():
    assert str(L("x")) == 'L("x")'


def test_negated_literal_str():
    assert str(~L("x")) == '~L("x")'


def _e(u):
    return re.sub(r"([()|])", r"\\\g<1>", u)


def _p(*us):
    return "(" + "|".join(_e(u) for u in us) + ")"


def test_and_formula_str():
    _test_str(
        L("x") & L("y"),
        _p('(L("x")) & (L("y"))', '(L("y")) & (L("x"))')
    )


def test_or_formula_str():
    _test_str(
        L("x") | L("y"),
        _p('(L("x") | L("y"))', '(L("y") | L("x"))')
    )


def test_and_formula_str_with_int_var():
    _test_str(
        L("x") & L(5),
        _p('(L("x")) & (L(5))', '(L(5)) & (L("x"))')
    )


def test_or_formula_str():
    _test_str(
        L("x") | L(5),
        _p('(L("x") | L(5))', '(L(5) | L("x"))')
    )
