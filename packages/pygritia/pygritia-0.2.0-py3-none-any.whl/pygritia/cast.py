"""
Provides :py:class:`CastAction` action class
It provides automatic conversion both direction evaluation and update.
"""
from typing import Any, Callable, Optional, TypeVar, cast
from dataclasses import dataclass
from .core import LazyMixin, LazyAction, LazyNS, evaluate, update, repr_
from .call import lazy_call


@dataclass
class CastAction(LazyAction):
    """Cast action"""
    __slots__ = ('expr_type', 'result_type', 'expr')

    expr_type: Any
    """Converter from result type to expression type"""
    result_type: Any
    """Converter from expression type to result type"""
    expr: Any
    """Target expression"""

    def __str__(self) -> str:
        result_type = getattr(self.result_type, '__name__', repr_(self.result_type))
        return f'{result_type}({repr_(self.expr)})'

    def evaluate(self, namespace: LazyNS) -> Any:
        return evaluate(self.result_type(self.expr), namespace)

    def update(self, val: Any, namespace: LazyNS) -> Any:
        if self.expr_type is None:
            expr_type = type(evaluate(self.expr, namespace))
        else:
            expr_type = self.expr_type
        update(self.expr, expr_type(val), namespace)


_T = TypeVar('_T')
_U = TypeVar('_U')


def lazy_cast(target_type: Callable[[_T], _U],
              expr: _T,
              expr_type: Optional[Callable[[_U], _T]] = None) -> _U:
    """
    Create automatic casting lazy expression

    :param target_type: Converter from expression type to result type
    :param expr: Target expression
    :param expr_type: Converter from result type to expression type

                      If it is omitted, the constructor of evaluated expr will be used.
    :return: Casting expression
    """
    if expr_type is not None:
        expr_type = lazy_call(expr_type)
    target_type = lazy_call(target_type)
    return cast(_U, LazyMixin.create(action=CastAction(expr_type, target_type, expr)))
