=================
Lite CNF Formulae
=================

This is module is intended to help with the building of smallish logical
statements.

Constructors
------------

**lite_cnf_formula.L(obj)**

Creates a new cnf_formula object with ``obj`` as the only literal

Methods and Operators
---------------------
Let ``A`` and ``B`` by cnf_formula objects

+--------------------------+----------------------------------------------------+
| ``A & B``                | Returns a new cnf_formula object that represents   |
|                          | the formula that is the result of anding the       |
|                          | formulae that A and B represent.                   |
+--------------------------+----------------------------------------------------+
| ``A | B``                | Returns a new cnf_formula object that represents   |
|                          | the formula that is the result of oring the        |
|                          | formulae that A and B represent                    |
+--------------------------+----------------------------------------------------+
| ``~ A``                  | Returns a cnf_formula object that represents the   |
|                          | formula that is the logical negation of the        |
|                          | formula that A represents                          |
+--------------------------+----------------------------------------------------+
| ``obj in A``             | Returns whether obj is a literal in the formula    |
|                          | that A represents. Equivelent to, but more         |
|                          | efficient than, obj in A.get_literals()            |
+--------------------------+----------------------------------------------------+
| ``obj x not in A``       | Returns whether obj is not a literal in the        |
|                          | formula that A represents. Equivelent to, but more |
|                          | efficient than, obj not in A.get_literals()        |
+--------------------------+----------------------------------------------------+
| ``A.get_literals()``     | Returns, as a frozenset, all the literals in the   |
|                          | formula that A represents                          |
+--------------------------+----------------------------------------------------+
| ``A.subsitute(obj, B)``  | Returns a new cnf_formula object that represents   |
|                          | the formula that A represents but with all         |
|                          | instances of the literal 'obj' replaced by the     |
|                          | formula that B represents.                         |
+--------------------------+----------------------------------------------------+

Constants
=========

**lite_cnf_formula.Tautology**

A constant that is cnf_formula object that represents a logical tautology.

**lite_cnf_formula.Contradiction**

A constant that is cnf_formula object that represents a logical condtriction.

cnf_formula Objects
===================
   
A cnf_formula object represents a Boolean formula in CNF. The precise
implemention of cnf_formula objects is not defined and is considered an
implementation detail. cnf_formula objects are immutable.


Utility Methods
===============

**lite_cnf_formula.is_cnf_formula(obj)**

Returns whether ``obj`` is a cnf_formula object

**lite_cnf_formula.or_(*objs)**

Shortcut that is equivelent to ``L(obj1) | L(obj2) | ...``

**lite_cnf_formula.and_(*objs)**

Shortcut that is equivelent to ``L(obj1) & L(obj2) & ...``

Example Usage
=============

::

  In [1]: from lite_cnf_formula import L, Tautology, Contradiction
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
  Out[9]: Contradiction
  In [9]: L('x') | ~L('x')
  Out[9]: Tautology
  In [10]: L('x') & Contradiction
  Out[10]: Contradiction 
  In [11]: L('a').substitute('a', L('b') & L('c'))
  Out[11]: ('b') & ('c')
  In [12]: (L('a') | L('b')).substitute('b', L('c') & L('d'))
  Out[12]: ('a' | 'c') & ('a' | 'd')
  In [13]: (L('a') | L('b')).substitute('b', Tautology)
  Out[13]: Tautology
  In [14]: (('a' | 'c') & ('a' | 'd')).get_literals()
  Out[14]: frozenset({'a','b','d'})
  In [15]: 'a' in (('a' | 'c') & ('a' | 'd'))
  Out[15]: True
