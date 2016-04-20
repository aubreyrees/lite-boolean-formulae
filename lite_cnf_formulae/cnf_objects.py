import itertools
import operator
import functools
from .utils.immutable_class import ImmutableClass
from .constants import Tautology, Contradiction


class CNFObj(ImmutableClass):
    def __and__(self, obj):
        if obj is Contradiction:
            return obj
        elif obj is Tautology:
            return self
        elif isinstance(obj, (L, CNFFormula)):
            return CNFFormula.build(self.clauses | obj.clauses)
        else:
            raise TypeError((
                "unsupported operand type(s) for &: '{}' and '{}'"
            ).format(self.__class__.__name__, obj.__class__.__name__))

    def __or__(self, obj):
        if obj is Contradiction:
            return self
        elif obj is Tautology:
            return obj
        elif isinstance(obj, (L, CNFFormula)):
            product = itertools.product(self.clauses, obj.clauses)
            return CNFFormula.build(x | y for x, y in product)
        else:
            raise TypeError((
                "unsupported operand type(s) for |: '{}' and '{}'"
            ).format(self.__class__.__name__, obj.__class__.__name__))


class CNFFormula(CNFObj):
    def __init__(self, clauses):
        self.clauses = clauses
        self._frozen = True

    @classmethod
    def build(cls, clauses):
        def build(singles, clauses):
            negated_singles = set(~s for s in singles)
            for s in clauses:
                if isinstance(s, CNFClause):
                    if len(s.vars) == 1 or s.vars.isdisjoint(singles):
                        yield CNFClause.build(s.vars - negated_singles)

        singles = set()
        clauses = set(clauses)

        for clause in clauses:
            if clause is Contradiction:
                return var
            elif isinstance(clause, CNFClause):
                if len(clause.vars) == 1:
                    var = next(iter(clause.vars))
                    if ~var in singles:
                        return Contradiction
                    else:
                        singles.add(var)

        formula = frozenset(build(singles, clauses))
        if formula:
            return cls(formula)
        else:
            return Tautology

    def __invert__(self):
        formulae = (~x for x in self.clauses)
        return functools.reduce(operator.or_, formulae)

    def substitute(self, var, formula):
        bits = (s.substitute(var, formula) for s in self.clauses)
        return functools.reduce(operator.and_, bits)

    def get_literals(self):
        bits = (s.get_literals() for s in self.clauses)
        return functools.reduce(operator.or_, bits)

    def __hash__(self):
        return hash(self.clauses)

    def __eq__(self, obj):
        return isinstance(obj, CNFFormula) and obj.clauses == self.clauses

    def __repr__(self):
        return '(' + ') & ('.join(repr(s) for s in self.clauses) + ')'

    def __contains__(self, obj):
        return any(obj in s for s in self.clauses)


class CNFClause(ImmutableClass):
    def __init__(self, vars):
        self.vars = vars
        self._frozen = True

    @classmethod
    def build(cls, vars):
        vars = set(vars)

        for var in vars:
            if var is Tautology:
                return var
            elif isinstance(var, L):
                if ~var in vars:
                    return Tautology

        clause = frozenset(v for v in vars if var is not Contradiction)

        if clause:
            return cls(clause)
        else:
            return Contradiction

    def __or__(self, obj):
        if obj is Contradiction:
            return self
        elif obj is Tautology:
            return obj
        elif isinstance(obj, CNFClause):
            clause = self.vars | obj.vars
            return CNFClause.build(clause)
        else:
            raise TypeError((
                "unsupported operand type(s) for |: '{}' and '{}'"
            ).format(self.__class__.__name__, obj.__class__.__name__))

    def __invert__(self):
        def build():
            for x in self.vars:
                yield CNFClause.build(set((~x,)))
        return CNFFormula.build(build())

    def substitute(self, var, formula):
        bits = (v.substitute(var, formula) for v in self.vars)
        return functools.reduce(operator.or_, bits)

    def get_literals(self):
        bits = (v.get_literals() for v in self.vars)
        return functools.reduce(operator.or_, bits)

    def __hash__(self):
        return hash(self.vars)

    def __eq__(self, obj):
        return (
            isinstance(obj, CNFClause) and
            obj.vars == self.vars
        )

    def __repr__(self):
        return ' | '.join(repr(s) for s in self.vars)

    def __contains__(self, obj):
        return any(obj in s for s in self.vars)


class L(CNFObj):
    def __init__(self, var, negated=False):
        self.var = var
        self.negated = negated
        self._frozen = True

    @property
    def clauses(self):
        return frozenset((CNFClause(frozenset((self,))),))

    def __invert__(self):
        return L(self.var, negated=(not self.negated))

    def substitute(self, var, formula):
        if self.var == var:
            if self.negated:
                return ~formula
            else:
                return formula
        else:
            return L(self.var, self.negated)

    def get_literals(self):
        return frozenset((self.var,))

    def __hash__(self):
        return int(str(hash(self.var)) + str(hash(self.negated)))

    def __eq__(self, obj):
        return (
            isinstance(obj, L) and
            self.var == obj.var and
            self.negated == obj.negated
        )

    def __repr__(self):
        if self.negated:
            return '~ {}'.format(repr(self.var))
        else:
            return repr(self.var)

    def __contains__(self, obj):
        return obj == self.var
