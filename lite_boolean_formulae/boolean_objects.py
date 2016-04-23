import itertools
import operator
import six
from .utils.pp import pp_class
from .utils.immutable_class import ImmutableClass


class StrCompatMixin(object):
    def __str__(self):
        out = self.__unicode__()
        if six.PY2:     # pragma: no cover
            out = out.encode("utf-8")
        return out


class CNFPublic(ImmutableClass, StrCompatMixin):
    def _type_error(self, c, obj):
        msg = 'Unsupported operand type(s) for {}: "{}" and "{}"'
        raise TypeError(msg.format(c, pp_class(self), pp_class(obj)))

    def __and__(self, obj):
        if obj is False:
            return obj
        elif obj is True:
            return self
        elif isinstance(obj, (L, CNFFormula)):
            return CNFFormula.build(self.clauses | obj.clauses)
        else:
            self._type_error("&", obj)

    def __or__(self, obj):
        if obj is False:
            return self
        elif obj is True:
            return obj
        elif isinstance(obj, (L, CNFFormula)):
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
            self._type_error("|", obj)

    def __xor__(self, obj):
        conjunction = self & obj
        disjunction = self | obj
        negated_conjunction = True if conjunction is False else ~conjunction
        return disjunction & negated_conjunction

    def __rand__(self, obj):
        return self.__and__(obj)

    def __ror__(self, obj):
        return self.__or__(obj)

    def __rxor__(self, obj):
        return self.__xor__(obj)


class CNFFormula(CNFPublic):
    def __init__(self, clauses):
        self.clauses = clauses
        self._frozen = True

    @classmethod
    def build(cls, clauses):
        def build(singles, clauses):
            negated_singles = set(~s for s in singles)
            for c in clauses:
                if len(c.literals) == 1 or c.literals.isdisjoint(singles):
                    yield CNFClause.build(c.literals - negated_singles)

        singles = set()
        clauses = set(clauses)

        for clause in clauses:
            if len(clause.literals) == 1:
                literal = next(iter(clause.literals))
                if ~literal in singles:
                    return False
                else:
                    singles.add(literal)

        return cls(frozenset(build(singles, clauses)))

    def __invert__(self):
        formulae = (~x for x in self.clauses)
        return six.moves.reduce(operator.or_, formulae)

    def __hash__(self):
        return hash(self.clauses)

    def __eq__(self, obj):
        return isinstance(obj, CNFFormula) and obj.clauses == self.clauses

    def __repr__(self):
        return '(' + ') & ('.join(repr(s) for s in self.clauses) + ')'

    def __contains__(self, obj):
        return any(obj in s for s in self.clauses)

    def __unicode__(self):
        clauses = u') & ('.join(six.text_type(s) for s in self.clauses)
        return u'({})'.format(clauses)

    def substitute(self, label, formula):
        bits = (c.substitute(label, formula) for c in self.clauses)
        return six.moves.reduce(operator.and_, bits)

    def get_literals(self):
        bits = (s.get_literals() for s in self.clauses)
        return six.moves.reduce(operator.or_, bits)


class CNFClause(ImmutableClass, StrCompatMixin):
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

    def __unicode__(self):
        literals = u' | '.join(six.text_type(l) for l in self.literals)
        return u'{}'.format(literals)

    def substitute(self, label, formula):
        bits = (l.substitute(label, formula) for l in self.literals)
        return six.moves.reduce(operator.or_, bits)

    def get_literals(self):
        bits = (v.get_literals() for v in self.literals)
        return six.moves.reduce(operator.or_, bits)


class L(CNFPublic):
    def __init__(self, label, negated=False):
        self.label = label
        self.negated = negated
        self._frozen = True

    def __invert__(self):
        return L(self.label, negated=(not self.negated))

    def __hash__(self):
        return hash(self.label) * 10 + (1 if self.negated else 0)

    def __eq__(self, obj):
        return (
            isinstance(obj, L) and
            self.label == obj.label and
            self.negated == obj.negated
        )

    def __repr__(self):
        if self.negated:
            return "~ L({})".format(repr(self.label))
        else:
            return "L({})".format(repr(self.label))

    def __contains__(self, obj):
        return obj == self.label

    def __unicode__(self):
        out = None

        text_label = six.text_type(self.label)
        if isinstance(self.label, six.string_types):
            out = u'L("{}")'.format(text_label.replace('"', '\\"'))
        else:
            out = u'L({})'.format(text_label)

        if self.negated:
            out = u"~" + out

        return out

    @property
    def clauses(self):
        return frozenset((CNFClause(frozenset((self,))),))

    def substitute(self, label, formula):
        if self.label == label:
            if self.negated:
                return ~formula
            else:
                return formula
        else:
            return L(self.label, self.negated)

    def get_literals(self):
        return frozenset((self.label,))
