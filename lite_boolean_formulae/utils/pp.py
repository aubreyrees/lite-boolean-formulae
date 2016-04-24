import inspect
import six


def pp_class(obj):
    """
    Prettify and return the passed class, or the class of the instance if an
    instance is passed in. 
    """
    if not inspect.isclass(obj):
        obj = obj.__class__

    if (
        (six.PY2 and obj.__module__ == "__builtin__") or
        (six.PY3 and obj.__module__ == "builtins")
    ):
        return "{}".format(obj.__name__)
    else:
        return "{}.{}".format(obj.__module__, obj.__name__)
