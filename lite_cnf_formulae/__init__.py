from .cnf_objects import L
from .constants import Tautology, Contradiction
from .shortcuts import is_cnf_formula, and_, or_

__all__ = [
    'L',
    'and_',
    'or_',
    'Tautology',
    'Contradiction',
    'is_cnf_formula'
]
