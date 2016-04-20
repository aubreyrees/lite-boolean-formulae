import pytest
from lite_boolean_formulae.utils.immutable_class import ImmutableClass


class Klass(ImmutableClass):
    pass


def test_set_class_attr():
    with pytest.raises(AttributeError):
        Klass.attr = "value"


def test_set_instance_attr_while_unfrozen():
    i = Klass()
    i.attr = "value"


def test_set_instance_attr_while_frozen():
    i = Klass()
    i._frozen = True
    with pytest.raises(AttributeError):
        i.attr = "value"
