import six
from .pp import pp_class


class ImmutableBase(type):
    """
    Any class that uses this base class as a metaclass cannot have class
    level attributes set on it.
    """
    def __setattr__(cls, name, value):
        raise AttributeError("Cannot alter '{}' class".format(pp_class(cls)))


@six.add_metaclass(ImmutableBase)
class ImmutableClass(object):
    """
    A class that should not be altered beyond its initial configuration.
    This is achived using a _frozen attribute that is set once __init__
    is run.
    """
    _frozen = False

    def __setattr__(self, name, value):
        if self._frozen:
            raise AttributeError(
                "Cannot alter instance of '{}'".format(pp_class(self))
            )
        else:
            super(ImmutableClass, self).__setattr__(name, value)
