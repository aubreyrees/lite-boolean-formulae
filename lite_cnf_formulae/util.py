from .cnf import CNFFormula, CNFLiteral

def is_cnf_formula(obj):
    """
    Returns whether obj is a cnf_formula object
    """
    return instance(obj, (CNFFormula, CNFLiteral))
