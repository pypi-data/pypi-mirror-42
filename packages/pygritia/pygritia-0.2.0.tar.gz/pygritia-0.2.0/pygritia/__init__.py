"""
=========================
Pygritia: Lazy Evaluation
=========================

* Build expressions naturally
* Evaluate expression with symbol substitution
* Create property by a expression with special symbol

>>> class Spam:
...     egg = [42]
...     foo = this.egg[0]
>>> spam = Spam()
>>> print(this.egg * 2)
this.egg * 2
>>> evaluate(this.egg * 2, {this: spam})
[42, 42]
>>> spam.foo
42
>>> spam.foo = 9
>>> spam.egg
[9]
"""
from .lazy import symbol
from .call import (lazy_call, lazy_delattr, lazy_delitem, lazy_getattr,
                   lazy_getitem, lazy_setattr, lazy_setitem)
from .core import evaluate, update
from .cases import (If, IfThenElse, Case, Ensure, is_none)
from .cast import lazy_cast
from .prop import this

__all__ = (
    'evaluate', 'lazy_call', 'lazy_delattr', 'lazy_delitem',
    'lazy_getattr', 'lazy_getitem', 'lazy_setattr',
    'lazy_setitem', 'symbol', 'update', 'this',
    'If', 'IfThenElse', 'Case', 'Ensure', 'is_none',
    'lazy_cast',
)
