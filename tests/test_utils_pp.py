from lite_boolean_formulae.utils import pp_class


class Klass(object):
    pass


def test_pp_class():
    assert pp_class(Klass) == "{}.Klass".format(Klass.__module__)


def test_pp_instance():
    assert pp_class(Klass()) == "{}.Klass".format(Klass.__module__)
