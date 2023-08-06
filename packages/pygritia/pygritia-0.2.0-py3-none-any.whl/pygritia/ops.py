"""
Provides :py:class:`Operator` lazy action class
It makes operators work well in lazy expression
"""
from typing import Any, Tuple, TypeVar, cast
import operator
from functools import wraps
from dataclasses import dataclass
from .util import FORWARD_OPERATORS
from .core import Lazy, LazyAction, LazyNS, evaluate, repr_


@dataclass
class Operator(LazyAction):
    """Operator applied expression"""
    __slots__ = ['operator', 'operands']

    operator: str
    operands: Tuple[Any, ...]

    def __str__(self) -> str:
        ops = FORWARD_OPERATORS[self.operator]
        if not ops.endswith('()') and len(self.operands) == 1:
            return ops + repr_(self.operands[0])
        if ops.endswith('()') or len(self.operands) > 2:
            opr = ops.strip('()')
            return '{}({})'.format(
                opr,
                ', '.join(
                    repr_(operand)
                    for operand in self.operands
                )
            )
        return ' '.join((repr_(self.operands[0]),
                         ops,
                         repr_(self.operands[1])))

    def evaluate(self, namespace: LazyNS) -> Any:
        return getattr(operator, self.operator)(
            *(evaluate(operand, namespace) for operand in self.operands))


_T = TypeVar('_T')

def lazy_operator(method: _T) -> _T:
    """
    Make given dunder method to lazy expression with :py:class:`Operator` action.
    """
    if callable(method) and hasattr(method, '__name__'):
        name = getattr(method, '__name__', '')

        @wraps(method)
        def wrapped(self: Lazy, *args: Any) -> Lazy:
            return self.__class__(action=Operator(name, (self,) + args), origin=self)
        return cast(_T, wrapped)
    raise TypeError(f"{method} is not a callable")


def lazy_roperator(method: _T) -> _T:
    """
    Make given dunder method to lazy expression with :py:class:`Operator` action.
    with reversed order
    """
    if callable(method) and hasattr(method, '__name__'):
        name = getattr(method, '__name__', '')
        name = '__' + name[3:]

        @wraps(method)
        def wrapped(self: Lazy, *args: Any) -> Lazy:
            return self.__class__(action=Operator(name, tuple(args) + (self,)), origin=self)
        return cast(_T, wrapped)
    raise TypeError(f"{method} is not a callable")
