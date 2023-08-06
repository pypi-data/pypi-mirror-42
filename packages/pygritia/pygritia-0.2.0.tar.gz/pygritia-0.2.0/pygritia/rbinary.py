"""
Provides :py:class:`ReversedBinaryMixin` mixin class
It provides reversed binary operator support to the :py:class:`Lazy` class
"""
from typing import Any
from .core import Lazy, LazyMixin
from .ops import lazy_roperator


class ReversedBinaryMixin(LazyMixin):
    """
    Reversed operator support

    It contains numeric operators(``__radd__``, ``__rsub__``, ``__rmul__``, ``__rmatmul__``,
    ``__rdiv__``, ``__rtruediv__``, ``__rfloordiv__``, ``__rmod__``, ``__rdivmod__``, ``__rpow__``)
    and bitwise operators(``__rlshift__``, ``__rrshift__``, ``__rand__``, ``__ror__``, ``__rxor__``)
    """

    @lazy_roperator
    def __radd__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rsub__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rmul__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rmatmul__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rdiv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rtruediv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rfloordiv__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rmod__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rdivmod__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rpow__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rlshift__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rrshift__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rand__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __rxor__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover

    @lazy_roperator
    def __ror__(self: Lazy, other: Any) -> Lazy:
        pass  # pragma: no cover
