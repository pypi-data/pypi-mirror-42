"""
Provides :py:class:`Lazy` class and :py:func:`symbol`
"""
from typing import Any, cast
from .symbols import Symbol
from .attr import AttrMixin
from .item import ItemMixin
from .call import CallMixin
from .unary import UnaryMixin
from .binary import BinaryMixin
from .rbinary import ReversedBinaryMixin


class Lazy(AttrMixin, ItemMixin, CallMixin, UnaryMixin,
           BinaryMixin, ReversedBinaryMixin):
    """
    Minimal base class of lazy expressions

    To extend functionality of lazy expressions(i.e. property descriptor from expression),
    create a new class which is derived from this class.

    Each functionality of :py:class:`Lazy` is implemented in the base mixin classes.
    """


def symbol(name: str) -> Any:
    """
    Create symbol for lazy expression

    :return: Newly created symbol expression
    :rtype: Any
    """
    return cast(Any, Lazy.create(action=Symbol(name)))
