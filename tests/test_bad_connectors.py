from lite_boolean_formulae import L
import pytest


def test_bad_conjunction():
    with pytest.raises(TypeError):
        L("x") & "x"


def test_bad_disunction():
    with pytest.raises(TypeError):
        L("x") | "x"
