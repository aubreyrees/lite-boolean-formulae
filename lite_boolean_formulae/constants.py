import sys
from .utils.immutable_class import ImmutableClass

class TautologyClass(ImmutableClass):
    _frozen = True

    def __and__(self, obj):
        return obj

    def __or__(self, obj):
        return self

    def __repr__(self):             # pragma: no cover
        return 'Tautology'

    def __invert__(self):
        return Contradiction

    def __hash__(self):
        return 1

    if sys.version_info < (3, 0):   # pragma: no cover
        def __unicode__(self):
            return u'Tautology'

        def __str__(self):
            return u'Tautology'.encode("utf-8")

        def __nonzero__(self):
            return True
    else:                           # pragma: no cover
        def __str__(self):
            return u'Tautology'

        def __bool__(self):
            return True


class ContradictionClass(ImmutableClass):
    _frozen = True

    def __and__(self, obj):
        return self

    def __or__(self, obj):
        return obj

    def __repr__(self):             # pragma: no cover
        return 'Contradiction'

    def __invert__(self):
        return Tautology

    def __hash__(self):
        return 0

    if sys.version_info < (3, 0):   # pragma: no cover
        def __unicode__(self):
            return u'Contradiction'

        def __str__(self):
            return u'Contradiction'.encode("utf-8")

        def __nonzero__(self):
            return False
    else:                           # pragma: no cover
        def __str__(self):
            return u'Contradiction'

        def __bool__(self):
            return False


Tautology = TautologyClass()
Contradiction = ContradictionClass()
