"""
Zoolander's color handling module.
"""
import operator

class HexMetaClass(type):
    OPERATORS = ("add", "sub", "mul", "div")

    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)

        def overload(op):
            """
            Overload this operator with a function that will take other
            instances of CssUnit, integers, or floats.
            """
            def overloaded_fn(self, other):
                my_class = type(self)
                op_fn = getattr(operator, op)
                if isinstance(other, my_class):
                    return my_class(hex(op_fn(self.num, other.num)))
                elif isinstance(other, int) or isinstance(other, float):
                    return my_class(hex(op_fn(self.num, other)))
                elif isinstance(other, str):
                    return my_class(hex(self.num + int(other, 16)))
                else:
                    raise TypeError("Unsupported types for %s, '%s' and '%s'" % (
                        str(op_fn), type(self), type(other)
                    ))
            return overloaded_fn

        for op in mcs.OPERATORS:
            setattr(cls, "__%s__" % op, overload(op))
            setattr(cls, "__r%s__" % op, "__%s__" % op)

        return cls


class Hex(object):
    __metaclass__ = HexMetaClass
    def __init__(self, hex_string):
        if hex_string[0] == "#":
            hex_string = hex_string[1:]
        self.num = int(hex_string, 16)
    def __str__(self):
        return "#%s" % hex(self.num).replace("0x", "")
