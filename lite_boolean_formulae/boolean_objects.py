import itertools
import operator
import six
import sys
from .utils.immutable_class import ImmutableClass
from .utils.pp import pp_class


class CNFPublic(ImmutableClass):
    def __and__(self, obj):
        if obj is False:
            return obj
        elif obj is True:
            return self
        elif isinstance(obj, (L, CNFFormula)):
            return CNFFormula.build(self.clauses | obj.clauses)
        else:
            raise TypeError((
                "unsupported operand type(s) for &: '{}' and '{}'"
            ).format(pp_class(self), pp_class(obj)))

    def __or__(self, obj):
        if obj is False:
            return self
        elif obj is True:
            return obj
        elif isinstance(obj, (L, CNFFormula)):
            product = itertools.product(self.clauses, obj.clauses)
            return CNFFormula.build(x | y for x, y in product)
        else:
            raise TypeError((
                "unsupported operand type(s) for |: '{}' and '{}'"
            ).format(pp_class(self), pp_class(obj)))

    def __rand__(self, obj):
        return self.__and__(obj)

    def __ror__(self, obj):
        return self.__or__(obj)


class CNFFormula(CNFPublic):
    def __init__(self, clauses):
        self.clauses = clauses
        self._frozen = True

    @classmethod
    def build(cls, clauses):
        def build(singles, clauses):
            negated_singles = set(~s for s in singles)
            for c in clauses:
                if isinstance(c, CNFClause):
                    if len(c.literals) == 1 or c.literals.isdisjoint(singles):
                        yield CNFClause.build(c.literals - negated_singles)

        singles = set()
        clauses = set(clauses)

        for clause in clauses:
            if clause is False:
                return var
            elif isinstance(clause, CNFClause):
                if len(clause.literals) == 1:
                    literal = next(iter(clause.literals))
                    if ~literal in singles:
                        return False
                    else:
                        singles.add(literal)

        formula = frozenset(build(singles, clauses))
        if formula:
            return cls(formula)
        else:
            return True

    def __invert__(self):
        formulae = (~x for x in self.clauses)
        return six.moves.reduce(operator.or_, formulae)

    def substitute(self, var, formula):
        bits = (c.substitute(var, formula) for c in self.clauses)
        return six.moves.reduce(operator.and_, bits)

    def get_literals(self):
        bits = (s.get_literals() for s in self.clauses)
        return six.moves.reduce(operator.or_, bits)

    def __hash__(self):
        return hash(self.clauses)

    def __eq__(self, obj):
        return isinstance(obj, CNFFormula) and obj.clauses == self.clauses

    def __repr__(self):
        return '(' + ') & ('.join(repr(s) for s in self.clauses) + ')'

    def __contains__(self, obj):
        return any(obj in s for s in self.clauses)

    if sys.version_info < (3, 0):   # pragma: no cover
        def __unicode__(self):
            clauses = u') & ('.join(unicode(s) for s in self.clauses)
            return u'({})'.format(clauses)

        def __str__(self):
            return unicode(self).encode("utf-8")
    else:   # pragma: no cover
        def __str__(self):
            clauses = u') & ('.join(str(s) for s in self.clauses)
            return u'({})'.format(clauses)


class CNFClause(ImmutableClass):
    def __init__(self, literals):
        self.literals = literals
        self._frozen = True

    @classmethod
    def build(cls, literals):
        for literal in literals:
            if ~literal in literals:
                return True

        return cls(frozenset(literals))

    def __or__(self, obj):
        return CNFClause.build(self.literals | obj.literals)

    def __invert__(self):
        def build():
            for x in self.literals:
                yield CNFClause.build(set((~x,)))
        return CNFFormula.build(build())

    def substitute(self, var, formula):
        bits = (l.substitute(var, formula) for l in self.literals)
        return six.moves.reduce(operator.or_, bits)

    def get_literals(self):
        bits = (v.get_literals() for v in self.literals)
        return six.moves.reduce(operator.or_, bits)

    def __hash__(self):
        return hash(self.literals)

    def __eq__(self, obj):
        return (
            isinstance(obj, CNFClause) and
            obj.literals == self.literals
        )

    def __repr__(self):
        return ' | '.join(repr(s) for s in self.literals)

    def __contains__(self, obj):
        return any(obj in s for s in self.literals)

    if sys.version_info < (3, 0):   # pragma: no cover
        def __unicode__(self):
            literals = u' | '.join(unicode(l) for l in self.literals)
            return u'({})'.format(literals)

        def __str__(self):
            return unicode(self).encode("utf-8")
    else:   # pragma: no cover
        def __str__(self):
            literals = u') | ('.join(str(l) for l in self.literals)
            return u'({})'.format(literals)


class L(CNFPublic):
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
        return hash(self.var) * 10 + (1 if self.negated else 0)

    def __eq__(self, obj):
        return (
            isinstance(obj, L) and
            self.var == obj.var and
            self.negated == obj.negated
        )

    def __repr__(self):
        if self.negated:
            return "~ L({})".format(repr(self.var))
        else:
            return "L({})".format(repr(self.var))

    def __contains__(self, obj):
        return obj == self.var


    if sys.version_info < (3, 0):   # pragma: no cover
        def __unicode__(self):
            out = None
            
            uvar = unicode(self.var)
            if isinstance(self.var, six.string_types):
                out = u'L("{}")'.format(uvar.replace('"', '\\"'))
            else:
                out = u'L({})'.format(uvar)

            if self.negated:
                out = u"~" + out

            return out

        def __str__(self):
            return unicode(self).encode("utf-8")
    else:   # pragma: no cover
        def __str__(self):
            out = None

            svar = str(self.var)
            if isinstance(self.var, six.string_types):
                out = u'L("{}")'.format(svar.replace('"', '\\"'))
            else:
                out = u'L({})'.format(svar)

            if self.negated:
                out = u"~" + out

            return out
