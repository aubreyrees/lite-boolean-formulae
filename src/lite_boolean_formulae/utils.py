"""Private module utlity functions."""


import inspect
from typing import TypeVar


T = TypeVar("T")


def frozenset_builder(*args: T) -> frozenset[T]:
    """Alternate frozenset constructor."""
    return frozenset(args)


def pp_class(obj: object) -> str:
    """
    Human readable class name.

    Prettify and return the passed class, or the class of the instance if an
    instance is passed in.
    """
    cls = obj if inspect.isclass(obj) else obj.__class__

    if cls.__module__ == "builtins":
        return f"{cls.__name__}"
    else:
        return f"{cls.__module__}.{cls.__name__}"
