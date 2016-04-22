import re
from lite_boolean_formulae import L
from .utils import _test_str, _test_repr


def test_repr_formula():
    _test_repr(L("x") & L("y"))


def test_repr_literal():
    _test_repr(L("x"))


def test_repr_negated_literal():
    _test_repr(~L("x"))


def test_literal_str():
    _test_str(L("x"), u'L\\("x"\\)')


def test_negated_literal_str():
    _test_str(~L("x"), u'~L\\("x"\\)')


def _e(u):
    return re.sub(r"([()|])", r"\\\g<1>", u)


def _p(*us):
    return u"(" + u"|".join(_e(u) for u in us) + u")"


def test_and_formula_str():
    _test_str(
        L("x") & L("y"),
        _p(u'((L("x"))) & ((L("y")))', u'((L("y"))) & ((L("x")))')
    )


def test_or_formula_str():
    _test_str(
        L("x") | L("y"),
        _p(u'((L("x")) | (L("y")))', u'((L("y")) | (L("x")))')
    )


def test_and_formula_str_with_int_var():
    _test_str(
        L("x") & L(5),
        _p(u'((L("x"))) & ((L(5)))', u'((L(5))) & ((L("x")))')
    )


def test_or_formula_str():
    _test_str(
        L("x") | L(5),
        _p(u'((L("x")) | (L(5)))', u'((L(5)) | (L("x")))')
    )
