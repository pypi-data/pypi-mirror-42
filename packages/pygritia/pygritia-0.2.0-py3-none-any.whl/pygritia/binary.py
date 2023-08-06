"""
Provides :py:class:`BinaryMixin` mixin class
It provides binary operator support to the :py:class:`Lazy` class
"""
from typing import Any
from .core import Lazy, LazyMixin
from .ops import lazy_operator


class BinaryMixin(LazyMixin):
    """
    Binary operator support

    It contains compare operators(``__lt__``, ``__le__``, ``__eq__``, ``__ne__``, ``__gt__``,
    ``_ge__``), numeric operators(``__add__``, ``__sub__``, ``__mul__``, ``__matmul__``,
    ``__div__``, ``__truediv__``, ``__floordiv__``, ``__mod__``, ``__divmod__``, ``__pow__``)
    and bitwise operators(``__lshift__``, ``__rshift__``, ``__and__``, ``__or__``, ``__xor__``)
    """
    @lazy_operator
    def __lt__(self, other: Any) -> bool:
        pass  # pragma: no cover

    @lazy_operator
    def __le__(self, other: Any) -> bool:
        pass  # pragma: no cover

    @lazy_operator
    def __eq__(self, other: Any) -> bool:
        pass  # pragma: no cover

    @lazy_operator
    def __ne__(self, other: Any) -> bool:
        pass  # pragma: no cover

    @lazy_operator
    def __gt__(self, other: Any) -> bool:
        pass  # pragma: no cover

    @lazy_operator
    def __ge__(self, other: Any) -> bool:
        pass  # pragma: no cover

    @lazy_operator
    def __add__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __sub__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __mul__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __matmul__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __div__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __truediv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __floordiv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __mod__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __divmod__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __pow__(self: Lazy, other: Any, *args: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __lshift__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __rshift__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __and__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __xor__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __or__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover
