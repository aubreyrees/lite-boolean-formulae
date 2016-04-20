import inspect


def pp_class(obj):
    if not inspect.isclass(obj):
        obj = obj.__class__

    return "{}.{}".format(obj.__module__, obj.__name__)
