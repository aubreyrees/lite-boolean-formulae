from .constants import TautologyClass, ContradictionClass


def is_boolean_formula(obj):
    """
    Returns whether obj is a boolean_formula object
    """
    from .boolean_objects import CNFFormula, L
    return isinstance(obj, (CNFFormula, L))


def is_tautology(obj):
    return isinstance(obj, TautologyClass)


def is_contradiction(obj):
    return isinstance(obj, ContradictionClass)
