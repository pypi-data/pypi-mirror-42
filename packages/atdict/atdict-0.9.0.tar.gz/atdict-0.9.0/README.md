[![PyPI version](https://badge.fury.io/py/atdict.svg)](https://badge.fury.io/py/atdict) [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.2576006.svg)](https://doi.org/10.5281/zenodo.2576006) [![Build Status](https://travis-ci.org/alphatwirl/atdict.svg?branch=master)](https://travis-ci.org/alphatwirl/atdict) [![codecov](https://codecov.io/gh/alphatwirl/atdict/branch/master/graph/badge.svg)](https://codecov.io/gh/alphatwirl/atdict)

# atdict

An attribute-access ordered dictionary in Python

*****

_atdict_ is an attribute-access ordered dictionary. You can use a key
name as an attribute to access the value of the dictionary for a key,
for example, `o.key_name` rather than `o['key_name']`. Only a minimum
set of methods are implemented so as to minimize the chances of name
conflicts.

_atdict_ was originally developed as the class
[`Object`](https://github.com/alphatwirl/scribblers/blob/v0.10.0/scribblers/obj.py)
in [_scribblers_](https://github.com/alphatwirl/scribblers), which
represents _event objects_ in
[_alphatwirl_](https://github.com/alphatwirl/alphatwirl). Since
`Object` became useful in other contexts, it was released as an
independent package as _atdict_.

*****

- [**Requirement**](#requirement)
- [**Install**](#install)
- [**How to use**](#how-to-use)
    - [Import atdict](#import-atdict)
    - [Initialize atdict](#initialize-atdict)
    - [Access to a value](#access-to-a-value)
    - [Modify a value](#modify-a-value)
    - [Add a key](#add-a-key)
    - [Delete a key](#delete-a-key)
    - [Copy and deepcopy](#copy-and-deepcopy)
    - [Pickle](#pickle)
- [**License**](#license)
- [**Contact**](#contact)

*****

## Requirement

- Python 2.7, 3.6, or 3.7

*****

## Install

You can install with `pip`.

```bash
$ pip install -U atdict
```

*****

## How to use

### Import atdict

Import `atdict` from the package `atdict`.

```python
from atdict import atdict
```

### Initialize atdict

You can initialize an `atdict` with any arguments that can initialize
[`collections.OrderedDict`](https://docs.python.org/3/library/collections.html#ordereddict-objects).

For example:
```python
o1 = atdict([('foo', 40), ('bar', 'ham')])
print(o1)
```

It will prints.

```python
atdict(foo=40, bar='ham')
```

An `atdict` can be also initialized with another `atdict`.

```
o2 = atdict(o1)
print(o2)
```

The `o2` is initialized with a (shallow) copy of the contents of `o1`.

```
atdict(foo=40, bar='ham')
```

### Access to a value

Yon can use a key name as an attribute of `atdict`.

```python
print(o1.foo)
```

This will print the value for the key `foo`, which is `40`.

```
40
```

### Modify a value

To modify a value, you can assign a new value to the attribute.

```python
o1.foo = 50
print(o1)
```

```
atdict(foo=50, bar='ham')
```

The value for the key `foo` changed from `40` to `50`.

### Add a key

To add a key, you can also assign a value to the attribute

```python
o1.baz = 'eggs'
print(o1)
```

```
atdict(foo=50, bar='ham', baz='eggs')
```

### Delete a key

`del` deletes a key.

```python
del o1.bar
print(o1)
```

```
atdict(foo=50, baz='eggs')
```

### Copy and deepcopy

A copy will be created if `atdict` is initialized with another
`atdict`. However, this will be a _shallow_ copy.

```python
l = [1, 2]
o1 = atdict([('foo', l)])
o2 = atdict(o1)
print(o2.foo is o1.foo)
```

```
True
```

To make a _deep_ copy, you can use `copy.deepcopy()`.

```python
import copy
l = [1, 2]
o1 = atdict([('foo', l)])
o2 = copy.deepcopy(o1)
print(o2)
```

```
atdict(foo=[1, 2])
```

`o2.foo` and `o1.foo` are not the same object.

```python
print(o2.foo is o1.foo)
```

```
False
```

### Pickle

An `atdict` is picklable as long as all values are picklable.

```python
import pickle
o1 = atdict([('foo', 40), ('bar', 'ham')])
p1 = pickle.dumps(o1)
o2 = pickle.loads(p1)
print(o2)
```

```
atdict(foo=40, bar='ham')
```


*****

## License

- atpbar is licensed under the BSD license.

*****

## Contact

- Tai Sakuma - tai.sakuma@gmail.com

