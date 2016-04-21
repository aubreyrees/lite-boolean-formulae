import operator
import functools
from .boolean_objects import L


def or_(*objs):
    """
    Shortcut method to or many variables togother
    """
    return functools.reduce(operator.or_, (L(o) for o in objs))


def and_(*objs):
    """
    Shortcut method to and many variables togother
    """
    return functools.reduce(operator.and_, (L(o) for o in objs))
