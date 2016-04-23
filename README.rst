=====================
Lite Boolean Formulae
=====================

This module helps with the building of smallish boolean formulae. This module
expresses boolean formulae in CNF internally.

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

Returns a new boolean_formula object (or a Boolean value if the
boolean_formula is tautology or contradiction) that is same as ``A`` but with
all instances of the literal with label ``obj`` replaced by ``B``.

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
  Out[2]: ('x' | 'y') & ('x' | 'z') 
  In [3]: L('x') | L('x')
  Out[3]: ('x')
  In [4]: ~ L('x')
  Out[4]: (~('x'))
  In [5]: ~ (~ L('x'))
  In [5]: ('x')
  In [6]: L('x') | (L('x') & L('y'))
  Out[6]: ('x')
  In [7]: L('x') | (L('~x') & L('y'))
  Out[7]: ('x' | 'y')
  In [8]: L('x') & (L('~x'))
  Out[9]: False
  In [9]: L('x') | ~L('x')
  Out[9]: True
  In [10]: L('x') & False
  Out[10]: False
  In [11]: L('a').substitute('a', L('b') & L('c'))
  Out[11]: ('b') & ('c')
  In [12]: (L('a') | L('b')).substitute('b', L('c') & L('d'))
  Out[12]: ('a' | 'c') & ('a' | 'd')
  In [13]: (L('a') | L('b')).substitute('b', True)
  Out[13]: True
  In [14]: ((L('a') | L('b')) & (L('a') | L('c'))).get_literals()
  Out[14]: frozenset({'a','b','c'})
  In [15]: 'a' in ((L('a') | L('c')) & (L('a') | L('d')))
  Out[15]: True
