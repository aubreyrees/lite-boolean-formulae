import operator
import functools
from .cnf import CNFLiteral

def and_(*objs):
    return functools.reduce(operator.and_, (L(o) for o in objs))

def or_(*objs):
    return functools.reduce(operator.or_, (L(o) for o in objs))

def L(var):
    return CNFLiteral(var, False)
