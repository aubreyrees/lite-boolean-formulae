"""Contains the classes used to build represent boolean formulae."""

import abc
import dataclasses
import functools
import itertools
import operator
from typing import Iterator, Iterable, Any, Self, TypeGuard, Hashable
from .utils import pp_class, frozenset_builder


def _type_error(c: str, o1: object, o2: object) -> TypeError:
    """Build a TypeError."""
    cls1: str = pp_class(o1)
    cls2: str = pp_class(o2)
    return TypeError(f'Unsupported operand type(s) for {c}: "{cls1}" and "{cls2}"')


class CNFPublicMixin(abc.ABC):
    """Mixin that provides &, | and ^ implementations."""

    @property
    @abc.abstractmethod
    def clauses(self: Self) -> frozenset["CNFClause"]:
        """Return all clauses in this boolean formula."""
        ...

    @abc.abstractmethod
    def __invert__(self: Self)  -> "bool | Self | CNFFormula | L":
        """Return the formula's negation."""
        ...

    def __and__(self: Self, obj: object) -> "bool | Self | CNFFormula | L":
        """Calculate the conjunction of the boolean objects."""
        if obj is False:
            return False
        elif obj is True:
            return self
        elif is_boolean_formula(obj):
            return CNFFormula.build(self.clauses | obj.clauses)
        else:
            raise _type_error("&", self, obj)

    def __or__(self: Self, obj: object) -> "bool | Self | CNFFormula | L":
        """Calculate the disjunction of the boolean objects."""
        if obj is False:
            return self
        elif obj is True:
            return True
        elif is_boolean_formula(obj):
            clauses = set()
            for x, y in itertools.product(self.clauses, obj.clauses):
                disjunction = x | y
                if disjunction is not True:
                    clauses.add(disjunction)
            if clauses:
                return CNFFormula.build(clauses)
            else:
                return True
        else:
            raise _type_error("|", self, obj)

    def __xor__(self: Self, obj: object) -> "bool | Self | CNFFormula | L":
        """Calculate the excludsive disjunction of the boolean objects."""
        if obj is True:
            return ~self
        elif obj is False:
            return self
        elif isinstance(obj, (L, CNFFormula)):
            conjunction = self & obj
            disjunction = self | obj
            if isinstance(conjunction, bool):
                if isinstance(disjunction, bool):
                    return disjunction and not conjunction
                else:
                    return (not conjunction) & disjunction
            else:
                return disjunction & ~conjunction
        else:
            raise _type_error( "^", self, obj)

    def __rand__(self: Self, obj: object) -> "bool | Self | CNFFormula | L":
        """Calculate the conjunction of the boolean objects."""
        return self.__and__(obj)

    def __ror__(self: Self, obj: object) -> "bool | Self | CNFFormula | L":
        """Calculate the disjunction of the boolean objects."""
        return self.__or__(obj)

    def __rxor__(self: Self, obj: object) -> "bool | Self | CNFFormula | L":
        """Calculate the excludsive disjunction of the boolean objects."""
        return self.__xor__(obj)


@dataclasses.dataclass(init=True,eq=True,frozen=True,slots=True)
class CNFFormula(CNFPublicMixin):
    """Represents a Boolean formula in CNF (a conjunction of clauses)."""

    clauses: frozenset[Any]

    @classmethod
    def build(
        cls, clauses: Iterable["CNFClause | bool"]
    ) -> "Self | bool | CNFFormula | L":
        """
        Build a formula using the passed clauses.

        This may return False if the resulting formula would be a contradiction.
        """
        def build(
            singles: set[L], clauses: set[CNFClause]
        ) -> Iterator[CNFClause | bool]:
            negated_singles = set(~s for s in singles)
            for c in clauses:
                if len(c.literals) == 1 or c.literals.isdisjoint(singles):
                    yield CNFClause.build(c.literals - negated_singles)

        singles: set[L] = set()
        final_clauses: set[CNFClause] = set()

        for clause in clauses:
            if isinstance(clause, bool):
                if not clause:
                    return False
            else:
                final_clauses.add(clause)
                if len(clause.literals) == 1:
                    literal = next(iter(clause.literals))
                    if ~literal in singles:
                        return False
                    else:
                        singles.add(literal)

        return cls(frozenset(build(singles, final_clauses)))

    def __invert__(self: Self) -> "bool | Self | CNFFormula | L":
        """Return the negation of the CNFFormula."""
        formulae = (~x for x in self.clauses)
        return functools.reduce(operator.or_, formulae)

    def __repr__(self: Self) -> str:
        """Return a string represenation of the CNFFormula for debugging."""
        inner: str = ') & ('.join(repr(s) for s in self.clauses)
        return f"({inner})"

    def __contains__(self: Self, obj: object) -> bool:
        """Return true if any literal in the formula has label ``obj``."""
        return any(obj in s for s in self.clauses)

    def __str__(self: Self) -> str:
        """Return a string represenation of the CNFFormula."""
        clauses = ') & ('.join(str(s) for s in self.clauses)
        return f'({clauses})'

    def substitute(
        self: Self,
        label: object,
        formula: Self | bool
    ) -> Self | bool:
        """Subsitute literals with label ``label`` with the formula ``formula``."""
        bits = (c.substitute(label, formula) for c in self.clauses)
        return functools.reduce(operator.and_, bits)

    def get_literals(self: Self) -> frozenset[object]:
        """Return the labels of all the literals in this formula."""
        bits = (s.get_literals() for s in self.clauses)
        return functools.reduce(operator.or_, bits)


@dataclasses.dataclass(init=True,eq=True,frozen=True,slots=True)
class CNFClause:
    """Represents a logical clause (a disjunction of literals)."""

    literals: frozenset["L"]

    @classmethod
    def build(cls, literals: Iterable["L"]) -> Self | bool:
        """
        Build a clause from the passed literals.

        This may return True if the combined clauses form a tautology.
        """
        for literal in literals:
            if ~literal in literals:
                return True

        return cls(frozenset(literals))

    def __or__(self: Self, obj: object) -> "CNFClause | bool":
        """Calculate the disjunction of the boolean objects."""
        if isinstance(obj, CNFClause):
            return CNFClause.build(self.literals | obj.literals)
        else:
            raise _type_error("|", self, obj)

    def __invert__(self: Self) ->  "Self | bool | CNFFormula | L":
        """Return the negation of the literal."""
        def build() -> Iterable[CNFClause | bool]:
            for x in self.literals:
                yield CNFClause.build(set((~x,)))
        return CNFFormula.build(build())

    def __repr__(self: Self) -> str:
        """Return a string represenation of the CNFClause for debugging."""
        return ' | '.join(repr(s) for s in self.literals)

    def __contains__(self: Self, obj: object) -> bool:
        """Return true if boolean formula has a literal with label ``obj``."""
        return any(obj in s for s in self.literals)

    def __str__(self: Self) -> str:
        """Return a string represenation of hte CNFClause."""
        literals = ' | '.join(str(x) for x in self.literals)
        return f'{literals}'

    def substitute(
        self: Self,
        label: object,
        formula: CNFFormula | bool
    ) -> "L | CNFFormula | bool":
        """Subsitute literals with label ``label`` with the formula ``formula``."""
        bits = (x.substitute(label, formula) for x in self.literals)
        return functools.reduce(operator.or_, bits)

    def get_literals(self: Self) -> frozenset[object]:
        """Return the labels of all the literals in this clause."""
        bits = (v.get_literals() for v in self.literals)
        return functools.reduce(operator.or_, bits)


@dataclasses.dataclass(init=True,eq=True,frozen=True,slots=True)
class L(CNFPublicMixin):
    """Represents a literal."""

    label: Hashable
    negated: bool = False

    def __invert__(self: Self) -> "L":
        """Return the negation of the literal."""
        return L(self.label, negated=(not self.negated))

    def __repr__(self: Self) -> str:
        """Return a string represenation of the literal for debugging."""
        rlabel: str = repr(self.label)
        if self.negated:
            return f"~L({rlabel})"
        else:
            return f"L({rlabel})"

    def __contains__(self: Self, obj: object) -> bool:
        """Return true if boolean formula has a literal with label ``obj``."""
        return obj == self.label

    def __str__(self: Self) -> str:
        """Return a string represenation of the literal."""
        out: str

        if isinstance(self.label, str):
            t = self.label.replace('"', '\\"')
            out = f'L("{t}")'
        else:
            t = str(self.label)
            out = f'L({t})'

        return f"~{out}" if self.negated else out

    @property
    def clauses(self: Self) -> frozenset[CNFClause]:
        """Return a CNFClause with this literal as the clause's sole literal."""
        return frozenset_builder(CNFClause(frozenset_builder(self)))

    def substitute(
        self: Self,
        label: object,
        formula: Self | CNFFormula | bool
    ) -> "L | bool | CNFFormula |  Self":
        """Subsitute literals with label ``label`` with the formula ``formula``."""
        if self.label == label:
            if self.negated:
                if isinstance(formula, bool):
                    return not formula
                else:
                    return ~formula
            else:
                return formula
        else:
            return L(self.label, self.negated)

    def get_literals(self: Self) -> frozenset[object]:
        """Return a frozenset containing only this literal's label."""
        return frozenset_builder(self.label)


def is_boolean_formula(obj: object) -> TypeGuard[CNFFormula | L]:
    """Return true if obj is a boolean_formula object."""
    return isinstance(obj, (CNFFormula, L))
