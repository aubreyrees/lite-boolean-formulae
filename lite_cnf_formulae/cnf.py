import itertools
import operator
import functools
from .base import ImmutableClass
from .constants import Tautology, Contradiction
from .internal_util import build_set

class CNFObj(ImmutableClass):
    def __and__(self, obj):
        if obj is Contradiction:
            return obj
        elif obj is Tautology:
            return self
        elif isinstance(obj, (CNFLiteral, CNFFormula)):
            return _cnf_formula(self.clauses | obj.clauses)
        else:
            raise TypeError((
                "unsupported operand type(s) for &: '{}' and '{}'"
            ).format(self.__class__.__name__, obj.__class__.__name__))

    def __or__(self, obj):
        if obj is Contradiction:
            return self
        elif obj is Tautology:
            return obj
        elif isinstance(obj, (CNFLiteral, CNFFormula)):
            product = itertools.product(self.clauses, obj.clauses)
            return _cnf_formula(x | y for x,y in product)
        else:
            raise TypeError((
                "unsupported operand type(s) for |: '{}' and '{}'"
            ).format(self.__class__.__name__, obj.__class__.__name__))

class CNFFormula(CNFObj):
    def __init__(self, clauses):
        self.clauses = clauses
        self._frozen = True

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

    def __or__(self, obj):
        if obj is Contradiction:
            return self
        elif obj is Tautology:
            return obj
        elif isinstance(obj, CNFClause):
            clause  = self.vars | obj.vars
            return _cnf_clause(clause)
        else:
            raise TypeError((
                "unsupported operand type(s) for |: '{}' and '{}'"
            ).format(self.__class__.__name__, obj.__class__.__name__))

    def __invert__(self):
        def build():
            for x in self.vars:
                yield _cnf_clause(set((~x,)))
        return _cnf_formula(build())

    def substitute(self, var, formula):
        bits = (v.substitute(var, formula) for v in self.vars)
        return functools.reduce(operator.or_, bits)

    def get_literals(self):
        bits = (v.get_literals() for v in self.vars)
        return functools.reduce(operator.or_, bits)

    def __hash__(self):
        return hash(self.vars)

    def __eq__(self, obj):
        return ( isinstance(obj, CNFClause)
                 and obj.vars == self.vars )

    def __repr__(self):
        return ' | '.join(repr(s) for s in self.vars)

    def __contains__(self, obj):
        return any(obj in s for s in self.vars)

class CNFLiteral(CNFObj):
    def __init__(self, var, negated):
        self.var = var
        self.negated = negated
        self._frozen = True

    @property
    def clauses(self):
        return build_set(CNFClause(build_set(self)))
   
    def __invert__(self):
        return CNFLiteral(self.var, negated = not self.negated)

    def substitute(self, var, formula):
        if self.var == var:
            if self.negated:
                return ~formula
            else:
                return formula
        else:
            return CNFLiteral(self.var, self.negated)

    def get_literals(self):
        return build_set(self.var)

    def __hash__(self):
        return int(str(hash(self.var)) + str(hash(self.negated)))

    def __eq__(self, obj):
        return ( isinstance(obj, CNFLiteral)
                 and self.var == obj.var
                 and self.negated == obj.negated )

    def __repr__(self):
        if self.negated:
            return '~ {}'.format(repr(self.var))
        else:
            return repr(self.var)

    def __contains__(self, obj):
        return obj == self.var

def _cnf_clause(vars):
    vars = set(vars)

    for var in vars:
        if var is Tautology:
            return var
        elif isinstance(var, CNFLiteral):
            if ~var in vars:
                return Tautology

    clause = frozenset(
        v for v in vars if not var is Contradiction)

    if clause:
        return CNFClause(clause)
    else:
        return Contradiction

def _cnf_formula(clauses):
    def build(singles, clauses):
        negated_singles = set(~s for s in singles)
        for s in clauses:
            if isinstance(s, CNFClause):
                if len(s.vars) == 1 or s.vars.isdisjoint(singles):
                    yield _cnf_clause(s.vars - negated_singles)

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
        return CNFFormula(formula)
    else:
        return Tautology
