from .internal_util import strclass

class Meta(type):
    def __setattr__(cls, name, value):
        raise AttributeError("Cannot alter '{}' class".format(strclass(cls)))

class ImmutableClass(object, metaclass = Meta):
    _frozen = False

    def __setattr__(self, name, value):
        if self._frozen:
            raise AttributeError("Cannot alter instance of '{}'".format(strclass(self.__class__)))
        else:
            super(ImmutableClass, self).__setattr__(name, value)
