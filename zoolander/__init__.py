"""
Zoolander - A Python DSL for generating Cascading Style Sheets.
"""
import operator
import traceback as tb

_CSS_TEMPLATE = """\
%s
%s {
%s
}"""

# Provide shorthand for commonly used words.
right = "right"
left = "left"
bold = "bold"
italic = "italic"
none = "none"
block = "block"
inline = "inline"

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

class _Definitions(object):
    def __init__(self):
        self.rules = {}
        self.selector_order = []

    def __enter__(self):
        def rule(*selectors, **properties):
            """
            Define a CSS rule for "selector" by passing keyword arguments.
            """
            selector = ",\n".join(selectors)

            if selector in self.rules:
                self.rules[selector].update(properties)
            else:
                self.rules[selector] = properties
                self.selector_order.append(selector)

                # XXX: Add definition line comment. Slightly hacky.
                stack = tb.extract_stack()
                self.rules[selector]["__COMMENT__"] = "/* Defined in %s, line %s */" % (
                    stack[0][0],
                    stack[0][1]
                )

        return rule

    def __exit__(*args):
        pass

class Stylesheet(object):
    def __init__(self):
        self.definitions = _Definitions()

    def render(self):
        """
        Render this Stylesheet object to a string of CSS.
        """
        css_accumulator = []

        for selector in self.definitions.selector_order:
            properties = self.definitions.rules[selector]
            comment = properties.pop("__COMMENT__")

            rendered_properties = "\n".join(
                ["    %s: %s;" % (key.replace("_", "-"), val)
                 for key, val in properties.items()]
            )

            css_accumulator.append(_CSS_TEMPLATE % (
                comment, selector, rendered_properties
            ))

        return "\n\n".join(css_accumulator)

    def render_to_file(self, filename):
        """
        Render this Stylesheet object to a file.
        """
        open(filename, "w").write(self.render())
        return self
