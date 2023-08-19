"""Contains the classes used to build represent boolean formulae."""

import abc
import dataclasses
import functools
import copy
import itertools
import operator
from typing import Iterator, Iterable, Any, Self, TypeGuard, Hashable, TypeVar
from .utils import pp_class, frozenset_builder


T = TypeVar("T", bound=Hashable)

def _type_error(c: str, o1: object, o2: object) -> TypeError:
    """Build a TypeError."""
    cls1: str = pp_class(o1)
    cls2: str = pp_class(o2)
    return TypeError(f'Unsupported operand type(s) for {c}: "{cls1}" and "{cls2}"')


def chain(x: Iterable[T] | None, y: Iterable[T] | None) -> frozenset[T] | None:
    if x is not None:
        if y is not None:
            return frozenset(itertools.chain(x, y))
        else:
            return  frozenset(x)
    elif y is not None:
        return frozenset(y)
    else:
        return None


def disjoint_or_none(s: frozenset[T] | None, t: frozenset[T] | None) -> bool:
    if s is None or t is None:
        return True
    else:
        return s.isdisjoint(t)


def copy_or_none(x: T | None) -> T | None:
    if x is None:
        return None
    else:
        return copy.copy(x)


class FormulaBaseClass(abc.ABC):
    pass


@dataclasses.dataclass(init=True,eq=True,frozen=True,slots=True)
class Formula(FormulaBaseClass):
    """Represents a boolean formula in CNF."""

    clauses: frozenset[tuple[frozenset[Hashable], frozenset[Hashable]]] | None
    unit_clauses: frozenset[Hashable] | None
    negated_unit_clauses: frozenset[Hashable] | None

    def __and__(self: Self, other: object) -> Self | bool:
        """Calculate the conjunction of the boolean formulae."""
        if other is False:
            return False
        elif other is True:
            return self
        elif isinstance(other, type(self)):
            if (
                disjoint_or_none(self.unit_clauses, other.negated_unit_clauses)
                or disjoint_or_none(other.unit_clauses, self.negated_unit_clauses)
            ):
                return type(self)(
                    clauses=chain(self.clauses, other.clauses),
                    unit_clauses=chain(self.unit_clauses, other.unit_clauses),
                    negated_unit_clauses=chain(
                         self.negated_unit_clauses, other.negated_unit_clauses
                    )
                )
            else:
                return False
        elif isinstance(other, L):
            unit_clauses: frozenset[Hashable] | None = None
            negated_unit_clauses: frozenset[Hashable] | None = None

            if other.negated:
                if self.unit_clauses is not None:
                    if other.label in self.unit_clauses:
                        return False
                    else:
                        unit_clauses=copy.copy(self.unit_clauses)

                if self.negated_unit_clauses is not None:
                    negated_unit_clauses=frozenset_builder(other, *self.negated_unit_clauses)
                else:
                    negated_unit_clauses=frozenset_builder(other)
            else:
                if self.negated_unit_clauses is not None:
                    if other.label in self.negated_unit_clauses:
                        return False
                    elif self.unit_clauses is None:
                        unit_clauses=frozenset_builder(other)
                    else:
                        unit_clauses=frozenset_builder(other, *self.unit_clauses)

                    negated_unit_clauses=copy.copy(self.negated_unit_clauses)

            return type(self)(
                clauses=copy_or_none(self.clauses),
                unit_clauses=unit_clauses,
                negated_unit_clauses=negated_unit_clauses
            )
        else:
            raise _type_error("&", self, other)


@dataclasses.dataclass(init=True,eq=True,frozen=True,slots=True)
class L(FormulaBaseClass):
    """Represents a literal."""

    label: Hashable
    negated: bool = False


def is_boolean_formula(obj: object) -> TypeGuard[Formula | L]:
    """Return true if obj is a boolean_formula object."""
    return isinstance(obj, (Formula, L))
