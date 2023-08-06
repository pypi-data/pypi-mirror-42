"""
Core functionality for lazy expressions
"""
from typing import Any, Mapping, Optional, Sequence, Type, TypeVar, Union, cast
from .util import setattr_


LazyNamespace = Mapping[Union[str, 'LazyMixin'], Any]
LazyNS = LazyNamespace


class LazyAction:
    """
    Lazy Expression Handler

    Every derived LazyAction classes must implements :py:meth:`evaluate` method.
    It is called by :py:func:`evaluate` function with given namespace
    """
    __slots__: Sequence[str] = ('owner',)
    owner: 'LazyMixin'
    """Owner lazy expression of this action"""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {str(self)}>"

    def evaluate(self, namespace: LazyNamespace) -> Any:
        """Evaluate expression

        To substitute actual value for specific symbol, give value with keyword argument.
        """
        raise NotImplementedError

    def update(self, val: Any, namespace: LazyNamespace) -> None:  # pylint: disable=no-self-use
        """Update value of expression

        If the expression is readonly, it raises AttributeError
        """
        raise AttributeError("expr cannot be updated")


class LazyMeta(type):
    """
    Metaclass for :py:class:`Lazy`

    It is for holding global :py:class:`Lazy` factory and creation
    """
    _factory: 'LazyType'

    @classmethod
    def register_factory(cls, lazy_factory: 'LazyType') -> 'LazyType':
        """
        Set global default :py:class:`Lazy` factory to ``lazy_factory``

        :param lazy_factory: New default lazy factory
        :type lazy_factory: Type[Lazy]
        :return: Old default lazy factory
        :rtype: Type[Lazy]
        """
        old, cls._factory = getattr(cls, '_factory', LazyMixin), lazy_factory
        return old

    @classmethod
    def create(cls, action: LazyAction, origin: Optional['LazyMixin'] = None) -> 'LazyMixin':
        """
        Create new lazy expression with given action by default lazy factory

        :param action: Evaluation/update handler for new lazy expression
        :type action: LazyAction
        :param origin: Lazy expression which cause creation of new expression
        :type origin: Optional[LazyMixin]
        :return: Newly created lazy expression
        :rtype: LazyMixin
        """
        return cls._factory(action=action, origin=origin)


class LazyMixin(metaclass=LazyMeta):
    """
    Base class of all lazy expression and mixin classes

    It provides *Protocol* for lazy expression

    All derived classes of this class have ``__hash__`` automatically, because namespace for
    evaluate is defined as lazy expression (normally symbol only) to value mapping. Key of
    mapping must be hashable.
    """
    __slots__: Sequence[str] = ('__action__', '__weakref__')
    __action__: LazyAction

    def __init_subclass__(cls) -> None:
        if '__hash__' not in cls.__dict__:
            def __hash__(self: LazyMixin) -> int:
                return hash(self.__action__)
            setattr(cls, '__hash__', __hash__)

    def __init__(self, action: LazyAction, origin: Optional['LazyMixin'] = None) -> None:
        del origin
        setattr_(self, '__action__', action)
        action.owner = self

    def __str__(self) -> str:
        return str(self.__action__)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {str(self)}>"


Lazy = TypeVar('Lazy', bound=LazyMixin)
LazyType = Type[LazyMixin]
_T = TypeVar('_T')


def evaluate(expr: _T, namespace: LazyNamespace) -> _T:
    """
    Evaluate lazy expression

    Evaluate expression with symbol substitution according to given ``namespace``

    :param expr: Lazy expression or evaluated value

                 If given value is not a lazy expression, this function returns it immediately
    :param namespace: Symbol table which will be used in substitution

                      The key of table can be both of string and symbol expression
    :return: Evaluated value
    """
    if isinstance(expr, LazyMixin):
        return cast(_T, expr.__action__.evaluate(namespace))
    return expr


def update(expr: _T, val: _T, namespace: LazyNamespace) -> None:
    """
    Update the value of lazy expression

    Set the value of lazy expression to the given ``val``
    Only *assignable expression* can be updated.
    ex) ``this[3]``, ``this.spam``

    :param expr: Assignable lazy expression
    :param val: New value
    :param namespace: Symbol table which will be used in substitution

                      The key of table can be both of string and symbol expression
    """
    if not isinstance(expr, LazyMixin):
        raise TypeError("Expr must be a lazy expression")
    val = evaluate(val, namespace)
    if isinstance(val, LazyMixin):
        raise TypeError("Val is not fully evaluated")
    expr.__action__.update(val, namespace)


def repr_(expr: Any) -> str:
    """
    ``repr()`` for lazy expression

    Native ``repr`` returns string like ``'<Lazy: this>'``. If you want to get the repr string
    like other objects, use this instead of native one. It returns expression only for lazy
    expression and ``repr()`` for other object.

    :param expr: object for repr
    :return: repr string of given object
    """
    if isinstance(expr, LazyMixin):
        return str(expr)
    return repr(expr)
