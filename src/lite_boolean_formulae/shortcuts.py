"""Shortcut functions for common tasks."""


import operator
import functools
from .boolean_objects import L, Formula


def or_(*objs: object) -> Formula | L | bool:
    """Return the disjunction of the passed literals."""
    return functools.reduce(operator.or_, (L(o, False) for o in objs))


def and_(*objs: object) -> Formula | L | bool:
    """Return the conjunction of the passed literals."""
    return functools.reduce(operator.and_, (L(o, False) for o in objs))
