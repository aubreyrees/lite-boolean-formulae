# Lite Boolean Formulae

This module provides ulities to build small Boolean formulae. This
module uses CNF internally and does not preserve the
formula.

## Installation

Suppored Python versions are: 3.11

To install using pip:

```
pip install git+https://github.com/aubreyrees/lite-booltean-formulae.git
```

You can obtain the source  from:

```
https://github.com/aubreyrees/lite-boolean-formulae
```

## Boolean formula Objects
   
This module implements objects that represent boolean formulae and these are built
up using literals. Literals are referenced using labels, where a label is any hashable
Python object. Two literals are equal if and only if there labels are equal.

Boolean formulae are immutable.


### Constructors

**lite_boolean_formulae.L(obj)**

Create a boolean formula consisting of only a literal with label `obj`.

### Methods and Operators

**A & B**

Calculate the conjunction of the formulae `A` and `B`.

**A | B**

Calculate the disjunction of the formulae `A` and `B`.

**A ^ B**

Calculate the exclusive disjunction of the formulae `A` and `B`.

**Note:** `&`, `|`, `^` are, as expected, associative
operations. A bool value be used as the left or right had value.

**\~A**

Returns the negation of the boolean formula `A`.

**obj in A**

`True` formula `A` contains a literal with label `obj`, else `False`.

**A.get_literals()**

Return a frozen containing the labels of all the literals in formula `A`.

**A.subsitute(obj, B)**

Create a new formula by replacing all literals with label `obj` with formula `B`.

### Utility Methods

**lite_boolean_formulae.is_boolean_formula(obj)**

`True` if `obj` is a boolean formula, else `False`.

**lite_boolean_formulae.or_(obj1, obj2, ...)**

Equivalent to `L(obj1) | L(obj2) | ...`.

**lite_boolean_formulae.and_(obj1, obj2, ...)**

Equivalent to `L(obj1) & L(obj2) & ...`.

### Example Usage

```
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
```

## Testing
Tests use tox and pytest. Make targets and build script provided for convience.

### Scripts

**scripts/make_venv**

Build a dev virtual enviroment (using the `venv` module) in the git repo root. This 
virtual enviroment will be used by make targets for packages.

### Makefile

Run `make help` to see targets.

### Testing with tox

Run `make tox` to install and run tox once the dev virtual enviroment is setup.

## Contributing
Contributions are welcome. Please ensure that any submitted code is well
tested.

## Authors
* Aubrey Rees
* Swin Purple (proof reader)

## License
lite-boolean-formula is licensed under the BSD license. See
LICENSE for the full license.
