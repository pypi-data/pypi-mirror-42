"""
Provides :py:class:`UnaryMixin` mixin class
It provides unary operator support to the :py:class:`Lazy` class
"""
from .core import Lazy, LazyMixin
from .ops import lazy_operator


class UnaryMixin(LazyMixin):
    """
    Binary operator support
    """
    @lazy_operator
    def __neg__(self: Lazy) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __pos__(self: Lazy) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __abs__(self: Lazy) -> Lazy:
        pass  # pragma: no cover

    @lazy_operator
    def __invert__(self: Lazy) -> Lazy:
        pass  # pragma: no cover
