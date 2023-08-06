"""Define some useful functions"""

# pylint: disable=invalid-name
getattr_ = object.__getattribute__
setattr_ = object.__setattr__
# pylint: enable=invalid-name


FORWARD_OPERATORS = {
    '__lt__': '<',
    '__le__': '<=',
    '__eq__': '==',
    '__ne__': '!=',
    '__gt__': '>',
    '__ge__': '>=',
    '__add__': '+',
    '__sub__': '-',
    '__mul__': '*',
    '__matmul__': '@',
    '__truediv__': '/',
    '__floordiv__': '//',
    '__mod__': '%',
    '__divmod__': 'divmod()',
    '__pow__': '**',
    '__lshift__': '<<',
    '__rshift__': '>>',
    '__and__': '&',
    '__xor__': '^',
    '__or__': '|',
    '__neg__': '-',
    '__pos__': '+',
    '__abs__': 'abs()',
    '__invert__': '~',
}

REVERSE_OPERATORS = {
    '__radd__': '__add__',
    '__rsub__': '__sub__',
    '__rmul__': '__mul__',
    '__rmatmul__': '__matmul__',
    '__rtruediv__': '__truediv__',
    '__rfloordiv__': '__floordiv__',
    '__rmod__': '__mod__',
    '__rdivmod__': '__divmod__',
    '__rpow__': '__pow__',
    '__rlshift__': '__lshift__',
    '__rrshift__': '__rshift__',
    '__rand__': '__and__',
    '__rxor__': '__xor__',
    '__ror__': '__or__',
}

OPERATORS = set(FORWARD_OPERATORS).union(set(REVERSE_OPERATORS))
