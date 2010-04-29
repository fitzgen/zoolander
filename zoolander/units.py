"""
This module has all of the css unit types.
"""
import operator

# Using a meta class for _Unit so that we don't have to define all the
# overloaded operators the exact same way, just with different operators. Using
# the operator module and a little magic, we can do this all at once.

class _UnitMetaClass(type):
    OPERATORS = ("add", "sub", "mul", "div")

    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)

        def overload(op):
            """
            Overload this operator with a function that will take other
            instances of _Unit, integers, or floats.
            """
            def overloaded_fn(self, other):
                my_class = type(self)
                op_fn = getattr(operator, op)
                if isinstance(other, my_class):
                    return my_class(op_fn(self.num, other.num))
                elif isinstance(other, int) or isinstance(other, float):
                    return my_class(op_fn(self.num, other))
                else:
                    raise TypeError("Unsupported types for %s, '%s' and '%s'" % (
                        str(op_fn), type(self), type(other)
                    ))
            return overloaded_fn

        for op in mcs.OPERATORS:
            setattr(cls, "__%s__" % op, overload(op))
            setattr(cls, "__r%s__" % op, "__%s__" % op)

        return cls

class _Unit(object):
    """
    Base class for all measurement units, such as em, px, and pt.

    Handles arithmetic for units.
    """
    __metaclass__ = _UnitMetaClass

    _UNIT = "meta unit"

    def __init__(self, num=0):
        self.num = num
    def __str__(self):
        return "%s%s" % (self.num, self._UNIT)

class em(_Unit):
    """The em unit."""
    _UNIT = "em"

class px(_Unit):
    """The px unit."""
    _UNIT = "px"

class pt(_Unit):
    """The pt unit."""
    _UNIT = "pt"

class pc(_Unit):
    """The pc unit."""
    _UNIT = "pc"

class in_(_Unit):
    """The inches unit."""
    _UNIT = "in"

class cm(_Unit):
    """The cm unit."""
    _UNIT = "cm"

class mm(_Unit):
    """The mm unit."""
    _UNIT = "mm"

class ex(_Unit):
    """The ex unit."""
    _UNIT = "ex"
