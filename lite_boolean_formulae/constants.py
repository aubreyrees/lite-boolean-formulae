from .utils.immutable_class import ImmutableClass


class TautologyClass(ImmutableClass):
    _frozen = True

    def __and__(self, obj):
        return obj

    def __or__(self, obj):
        return self

    def __bool__(self):
        return True

    def __repr__(self):
        return 'Tautology'

    def __invert__(self):
        return Contradiction


class ContradictionClass(ImmutableClass):
    _frozen = True

    def __and__(self, obj):
        return self

    def __or__(self, obj):
        return obj

    def __bool__(self):
        return False

    def __repr__(self):
        return 'Contradiction'

    def __invert__(self):
        return Tautology


Tautology = TautologyClass()
Contradiction = ContradictionClass()
