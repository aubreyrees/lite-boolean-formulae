import re
import six
import sys


def _test_str(cls, r, u=None):
    if (2,6) < sys.version_info and sys.version_info < (2,8):
        #assert re.match(r"^" + r + r"$", str(cls).decode("utf-8"))
        assert re.match(r"^" + r + r"$", unicode(cls))
    elif (3,2) < sys.version_info and sys.version_info < (3,6):
        assert re.match(u"^" + r + u"$", str(cls))
    else:
        raise Exception("Unsupported version")


def _test_repr(obj):
    assert isinstance(repr(obj), six.string_types)
