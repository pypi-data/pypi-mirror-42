"""
Provides :py:class:`CallMixin` mixin class
It provides call support to the :py:class:`Lazy` class
"""
from typing import Any, Mapping, Tuple, TypeVar, cast
from functools import wraps
import operator
from dataclasses import dataclass
from .core import Lazy, LazyAction, LazyMixin, LazyNS, evaluate, repr_


@dataclass
class Call(LazyAction):
    """Function call"""
    __slots__ = ['target', 'args', 'kwargs']

    target: Any
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __str__(self) -> str:
        if isinstance(self.target, LazyMixin):
            name = str(self.target)
        elif hasattr(self.target, '__name__'):
            name = self.target.__name__
        else:
            name = repr(self.target)
        return '{}({})'.format(
            name,
            ', '.join(
                item
                for items in (
                    (repr_(arg) for arg in self.args),
                    (key + '=' + repr_(value) for key, value in self.kwargs.items())
                )
                for item in items
            )
        )

    def evaluate(self, namespace: LazyNS) -> Any:
        callable_ = evaluate(self.target, namespace)
        args_ = (evaluate(arg, namespace) for arg in self.args)
        kwargs_ = {key: evaluate(value, namespace) for key, value in self.kwargs.items()}
        return callable_(*args_, **kwargs_)


class CallMixin(LazyMixin):
    """
    Call support

    Function call is read only expression
    """
    def __call__(self: Lazy, *args: Any, **kwargs: Any) -> Lazy:
        return self.__class__(action=Call(self, args, kwargs), origin=self)


_T = TypeVar('_T')

def lazy_call(func: _T) -> _T:
    """
    Make a function to support lazy expression

    >>> from pygritia import this, lazy_call, evaluate
    >>> @lazy_call
    ... def hello(obj):
    ...     print(obj)
    >>> print(hello(this))
    hello(this)
    >>> hello("123")
    123
    >>> evaluate(hello(this), {this: "123"})
    123
    """
    if callable(func):
        func_ = func

        @wraps(func)
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            lazy = any(
                isinstance(arg, LazyMixin)
                for arglist in (args, kwargs.values())
                for arg in arglist
            )
            if lazy:
                return LazyMixin.create(action=Call(func_, args, kwargs))
            return func_(*args, **kwargs)
        return cast(_T, wrapped)
    raise TypeError("lazy_call must be applied to callable")


# pylint: disable=invalid-name
lazy_getitem = lazy_call(operator.getitem)
"Lazy expression version of getitem"
lazy_setitem = lazy_call(operator.setitem)
"Lazy expression version of setitem"
lazy_delitem = lazy_call(operator.delitem)
"Lazy expression version of delitem"
lazy_getattr = lazy_call(getattr)
"Lazy expression version of getattr"
lazy_setattr = lazy_call(setattr)
"Lazy expression version of setattr"
lazy_delattr = lazy_call(delattr)
"Lazy expression version of delattr"
# pylint: enable=invalid-name
