"""
Provides :py:class:`LazyProp` class
"""
from typing import Any, Type, Optional
from .core import LazyAction, LazyMixin, evaluate, update
from .lazy import Lazy, symbol
from .util import setattr_


class LazyProp(Lazy):
    """
    `LazyProp` makes lazy expression as a descriptor

    >>> class A:
    ...     hello = "hello"
    ...     world = this.hello + ", world!"
    >>> A().world
    hello, world!
    """
    def __init__(self, action: LazyAction, origin: Optional[LazyMixin] = None) -> None:
        super().__init__(action, origin)
        setattr_(self, '__doc__', str(self))

    def __get__(self, inst: Any, owner: Type[Any]) -> Any:
        if inst is None:
            return self
        return evaluate(self, {this: inst})

    def __set__(self, inst: Any, value: Any) -> None:
        update(self, value, {this: inst})

Lazy.register_factory(LazyProp)

this = symbol('this')  # pylint: disable=invalid-name
"""Entry point of :py:class:`LazyProp`"""
