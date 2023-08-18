"""
Package provides utilities to build small Boolean formulae.

* L - this class wraps any Python object and represents a literal with the wrapped
       object as it's label.
* and_, or_ - convience methods for building conjunctions and disjunctions of literals.
* is_boolean_formula: type guard that returns true if an object is a boolean formula.
"""

from .boolean_objects import L, is_boolean_formula
from .shortcuts import and_, or_

__all__ = ["L", "and_", "or_", "is_boolean_formula"]
