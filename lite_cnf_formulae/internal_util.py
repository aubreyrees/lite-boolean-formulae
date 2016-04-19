def build_set(var):
    return frozenset((var,))

def strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__name__)
