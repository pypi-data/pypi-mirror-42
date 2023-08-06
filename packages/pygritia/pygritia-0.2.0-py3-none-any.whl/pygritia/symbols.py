"""
Provides :py:class:`Symbol` lazy action class
It makes operators work well in lazy expression

Action :py:class:`Symbol` does not have corresponding LazyMixin class, because symbol does not
need any additional feature to lazy expression.
"""
from typing import Any
from dataclasses import dataclass
from .core import LazyAction, LazyNS


@dataclass
class Symbol(LazyAction):
    """Symbol accessor"""

    __slots__ = ['name']
    name: str

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return id(self)

    def evaluate(self, namespace: LazyNS) -> Any:
        expr = self.owner
        if expr in namespace:
            return namespace[expr]
        if self.name in namespace:
            return namespace[self.name]
        return expr
