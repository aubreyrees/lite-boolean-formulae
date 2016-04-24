import six


class StrCompatMixin(object):
    """
    A mixin that implements a __str__ method that will return either unicode
    if using python 3 or an encoded unicode string if using python 2
    """
    def __str__(self):
        out = self.__unicode__()
        if six.PY2:     # pragma: no cover
            out = out.encode("utf-8")
        return out


