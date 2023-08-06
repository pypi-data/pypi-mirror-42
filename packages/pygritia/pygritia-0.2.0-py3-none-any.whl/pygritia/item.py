"""
Provides :py:class:`ItemMixin` mixin class
It provides item accessor support to the :py:class:`Lazy` class
"""
from typing import Any
from dataclasses import dataclass
from .core import Lazy, LazyAction, LazyMixin, LazyNS, evaluate, repr_


@dataclass
class Item(LazyAction):
    """Item accessor"""
    __slots__ = ['target', 'index']

    target: Any
    index: Any

    def __str__(self) -> str:
        target = repr_(self.target)
        index = repr_(self.index)
        if isinstance(self.index, slice):
            idx_ = ([repr_(self.index.start) if self.index.start is not None else '',
                     repr_(self.index.stop) if self.index.stop is not None else ''] +
                    ([repr_(self.index.step)] if self.index.step is not None else []))
            index = ':'.join(idx_)
        return f'{target}[{index}]'

    def evaluate(self, namespace: LazyNS) -> Any:
        return evaluate(self.target, namespace)[evaluate(self.index, namespace)]

    def update(self, val: Any, namespace: LazyNS) -> None:
        obj = evaluate(self.target, namespace)
        index = evaluate(self.index, namespace)
        obj[index] = val


class ItemMixin(LazyMixin):
    """
    Attribute access support

    Substitution to lazy expression is not supported

    *NOTICE*: Dunder magic methods are not lazily evaluated and applied to expression object.
    """
    def __getitem__(self: Lazy, idx: Any) -> Lazy:
        return self.__class__(action=Item(self, idx), origin=self)
