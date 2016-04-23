=====================
Lite Boolean Formulae
=====================

This module helps with the building of smallish boolean formulae. This module
expresses boolean formulae in CNF internally and does not preserve the
original form of the formula.

**Contents**

* `Installation`_
* `boolean_formula Objects`_
  - `Constructors`_
  - `Methods and Operators`_
* `Utility Methods`_
* `Example Usage`_
* `Testing`_
* `Contributing`_
* `Authors`_
* `License`_

Installation
============

Suppored Python versions are: 2.7, 3.3, 3.4 and 3.5 

To install using pip:

::

    pip install git+https://github.com/aubreystarktoller/lite-booltean-formulae.git

You can obtain the source  from:

::

    https://github.com/aubreystarktoller/lite-boolean-formulae

boolean_formula Objects
=======================
   
A boolean_formula object represents a Boolean formula. The precise
implemention of a boolean_formula object is not defined and is considered an
implementation detail, but they do consist of literals which are referenced
using labels, where a label is any hashable Python object. It is assumed that
if two literals have the same label they are the same.

boolean_formula objects are immutable.


Constructors
------------

**lite_boolean_formulae.L(obj)**

Creates a new boolean_formula object with a single literal
with ``obj`` as it's label.

Methods and Operators
---------------------
Let ``A`` be a boolean_formula object and let ``B`` be either a
boolean_formula object or a Boolean value.

**A & B**

Returns either a boolean_formula object or a Boolean value that is
the result anding ``A`` and ``B`` together.

**A | B**

Returns either a boolean_formula object or a Boolean value that is
the result of oring ``A`` and ``B``.

**A ^ B**

Returns either a boolean_formula object or a Boolean value that is
the result of xoring ``A`` and ``B``.

**Note:** ``&``, ``|``, ``^`` are, as one would expected, associative
operations.  Also a Boolean value can either side of the operator -
boolean_formula objects support right hand side logical operations.


**~ A**

Returns a new boolean_formula object that is the negation of ``A``.

**obj in A**

Returns ``True`` if a literal with label ``obj`` is in ``A``, and ``False``
otherwise. Equivelent to, but more efficient than,
``obj not in A.get_literals()``.

**obj x not in A**

Returns ``True`` if a literal with label ``obj`` is not in ``A``, and 
``False`` otherwise. Equivelent to, but more efficient than,
``obj not in A.get_literals()``.

**A.get_literals()**

Returns, as a frozenset, the labels of all the literals in ``A``.

**A.subsitute(obj, B)**

Returns a new boolean_formula object (or a Boolean value if the resulting
boolean_formula is tautology or contradiction) that is the same as ``A`` but
with all instances of the literal with label ``obj`` replaced by ``B``.

Utility Methods
===============

**lite_boolean_formulae.is_boolean_formula(obj)**

Returns ``True`` if ``obj`` is a boolean_formula object, and ``False``
otherwise.

**lite_boolean_formulae.or_(obj1, obj2, ...)**

Shortcut that is equivelent to ``L(obj1) | L(obj2) | ...``.

**lite_boolean_formulae.and_(obj1, obj2, ...)**

Shortcut that is equivelent to ``L(obj1) & L(obj2) & ...``.

Example Usage
=============

::

  In [1]: from lite_boolean_formulae import L
  In [2]: L('x') | (L('y') & L('z'))
  Out[2]: (L('x') | L('y')) & (L('x') | L('z')) 
  In [3]: L('x') | L('x')
  Out[3]: (L('x'))
  In [4]: ~L('x')
  Out[4]: ~ L('x')
  In [5]: ~(~L('x'))
  In [5]: L('x')
  In [6]: L('x') | (L('x') & L('y'))
  Out[6]: (L('x'))
  In [7]: L('x') | (~L('x') & L('y'))
  Out[7]: (L('x') | L('y'))
  In [8]: L('x') & (L('~x'))
  Out[9]: False
  In [9]: L('x') | ~L('x')
  Out[9]: True
  In [10]: L('x') & False
  Out[10]: False
  In [11]: L('x').substitute('x', L('y') & L('z'))
  Out[11]: (L('y')) & (L('z'))
  In [12]: (L('w') | L('x')).substitute('x', L('y') & L('z'))
  Out[12]: (L('w') | L('y')) & (L('w') | L('z'))
  In [13]: (L('x') | L('y')).substitute('y', True)
  Out[13]: True
  In [14]: ((L('x') | L('y')) & (L('x') | L('z'))).get_literals()
  Out[14]: frozenset({'x','y','z'})
  In [15]: 'x' in ((L('x') | L('y')) & (L('x') | L('z')))
  Out[15]: True

Testing
=======

To run the tests first clone the git repo and enter the cloned repo:

::

    git clone https://github.com/aubreystarktoller/django-babik-shadow-accounts
    cd django-babik-shadow-accounts

To run the tests you'll require ``make``. It is recommended that use tox to run
the tests:

::

    tox

To run the tests in the current environment:

::

    make test

Contributing
============

Contributions are welcome. Please ensure the any submitted code is well
tested.

If you think you have found a security venerability in the code please report
it **privately** by e-mailing Aubrey Stark-Toller at aubrey@deepearth.uk.

Please **do not** raise it on the issue tracker, or publicly at all, until I
have had a chance to look into it.

Authors
=======
Aubrey Stark-Toller

License
=======
``django-babik-shadow-accounts`` is licensed under the BSD license. See
LICENSE for the full license
