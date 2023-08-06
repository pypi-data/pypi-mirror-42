"""
Provides :py:class:`CasesAction` action class
It provides several assignable conditional expression
"""
from typing import Any, Mapping, Optional, TypeVar, Union, cast
from dataclasses import dataclass
from .core import LazyAction, LazyNS, evaluate, update, repr_
from .call import lazy_call
from .lazy import Lazy


@dataclass
class CasesAction(LazyAction):
    """Cases action"""
    __slots__ = ('condition', 'cases', 'default')

    condition: Any
    """Condition"""
    cases: Mapping[Any, Any]
    """Condition to value mapping"""
    default: Any
    """Default value when no case is matched"""

    def __str__(self) -> str:
        condition = repr_(self.condition)
        if len(self.cases) == 1:
            if condition[:5] == 'bool(' and condition[-1] == ')':
                condition = condition[5:-1]
            elif condition[:8] == 'is_none(' and condition[-1] == ')':
                if condition[8:-1] == repr_(self.default):
                    return f'Ensure({condition[8:-1]})'
            cond, value = tuple(self.cases.items())[0]
            if cond is True:
                cond_ = ''
            else:
                cond_ = f' == {repr_(cond)}'

            if self.default is None:
                return f'If({condition}{cond_}, {repr_(value)})'
            return (f'IfThenElse({condition}{cond_}, '
                    f'{repr_(value)}, {repr_(self.default)})')
        return (f'Case({condition}, {{' +
                ', '.join(f'{repr_(cond)}: {repr_(value)}'
                          for cond, value in self.cases.items()) +
                f'}}, {repr_(self.default)})')

    def evaluate(self, namespace: LazyNS) -> Any:
        cond = evaluate(self.condition, namespace)
        for key, value in self.cases.items():
            if evaluate(key, namespace) == cond:
                return evaluate(value, namespace)
        return evaluate(self.default, namespace)

    def update(self, val: Any, namespace: LazyNS) -> None:
        cond = evaluate(self.condition, namespace)
        for key, value in self.cases.items():
            if evaluate(key, namespace) == cond:
                update(value, val, namespace)
                break
        else:
            update(self.default, val, namespace)


_T = TypeVar('_T')
_U = TypeVar('_U')


# pylint: disable=invalid-name
_bool = lazy_call(bool)


def If(cond: bool, value: _T) -> Optional[_T]:
    """value if cond else None"""
    return cast(_T, Lazy.create(action=CasesAction(_bool(cond), {True: value}, None)))

def IfThenElse(cond: bool, true: _T, false: _U) -> Union[_T, _U]:
    """true if cond else false"""
    return cast(_T, Lazy.create(action=CasesAction(_bool(cond), {True: true}, false)))

def Case(cond: _T, cases: Mapping[_T, _U], default: _U) -> _U:
    """cases.get(cond, default)"""
    return cast(_U, Lazy.create(action=CasesAction(cond, cases, default)))

@lazy_call
def is_none(obj: Any) -> bool:
    """obj is None"""
    return obj is None

def Ensure(obj: Optional[_T], default: _T) -> _T:
    """obj if obj is not None else default"""
    return cast(_T, Lazy.create(action=CasesAction(is_none(obj), {True: default}, obj)))
# pylint: enable=invalid-name

__all__ = ('If', 'IfThenElse', 'Case', 'is_none', 'Ensure')
