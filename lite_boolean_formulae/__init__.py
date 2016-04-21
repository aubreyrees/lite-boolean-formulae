from .boolean_objects import L
from .constants import Tautology, Contradiction
from .shortcuts import and_, or_
from .checks import is_boolean_formula, is_tautology, is_contradiction

__all__ = [
    "L",
    "and_",
    "or_",
    "Tautology",
    "Contradiction",
    "is_boolean_formula"
    "is_tautology",
    "is_contradiction",
]
