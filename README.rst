=====================
Lite Boolean Formulae
=====================

This module helps with the building of smallish boolean formulae. This module
expresses boolean formulae in CNF internally.

boolean_formula Objects
=======================
   
A boolean_formula object represents a Boolean formula. The precise
implemention of a boolean_formula object is not defined and is considered an
implementation detail. boolean_formula objects are immutable.


Constructors
------------

**lite_boolean_formulae.L(obj)**

Creates a new boolean_formula object with ``obj`` as the only literal.

Methods and Operators
---------------------
Let ``A`` and ``B`` by boolean_formula objects

+--------------------------+-------------------------------------------------+
| ``A & B``                | Returns a new boolean_formula object that       |
|                          | represents the formula that is the result of    |
|                          | anding the formulae that ``A`` and ``B``        |
|                          | represent.                                      |
+--------------------------+-------------------------------------------------+
| ``A | B``                | Returns a new boolean_formula object that       |
|                          | represents the formula that is the result of    |
|                          | oring the formulae that ``A`` and ``B``         |
|                          | represent.                                      |
+--------------------------+-------------------------------------------------+
| ``~ A``                  | Returns a new boolean_formula object that       |
|                          | reprsents the formula that is the logical       |
|                          | negation of the formula that ``A`` represents.  |
+--------------------------+-------------------------------------------------+
| ``obj in A``             | Returns whether ``obj`` is a literal in the     |
|                          | formula that ``A`` represents. Equivelent to,   |
|                          | but more efficient than,                        |
|                          | ``obj in A.get_literals()``                     |
+--------------------------+-------------------------------------------------+
| ``obj x not in A``       | Returns whether ``obj`` is not a literal in the |
|                          | formula that ``A`` represents. Equivelent to,   |
|                          | but more efficient than,                        | 
|                          | ``obj not in A.get_literals()``                 |
+--------------------------+-------------------------------------------------+
| ``A.get_literals()``     | Returns, as a frozenset, all the literals in    |
|                          | the formula that ``A`` represents               |
+--------------------------+-------------------------------------------------+
| ``A.subsitute(obj, B)``  | Returns a new boolean_formula object that       |
|                          | represents the formula that ``A`` represents    |
|                          | but with all instances of the literal ``obj``   |
|                          | replaced by the formula that ``B`` represents.  |
+--------------------------+-------------------------------------------------+

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
