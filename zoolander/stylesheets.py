"""
Zoolander's main stylesheet rendering logic.
"""
import traceback as tb
from colors import *
from units import *
from shorthand import *

_CSS_TEMPLATE = """\
%s
%s {
%s
}"""

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

def _is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

class Stylesheet(object):

    # The following atomic types can be rendered directly to a CSS value and
    # don't need any manipulation.
    _ATOMIC_CSS_VALUE_TYPES = (str, int, float, CssUnit, Hex)

    def __init__(self):
        self.definitions = _Definitions()

    def _is_atomic_css_type(self, obj):
        """Return bool based on if obj can be rendered to CSS as-is."""
        return any(isinstance(obj, type_)
                   for type_ in self._ATOMIC_CSS_VALUE_TYPES)

    def _render_css_item(self, attr, val):
        """
        Render a single key/val pair.
        """
        css_attr = attr.replace("_", "-")

        if self._is_atomic_css_type(val):
            css_val = val
        elif _is_iterable(val):
            css_val = " ".join(map(str, val))
        else:
            raise TypeError("Unsupported CSS value: %s" % val)

        return "    %s: %s;" % (css_attr, css_val)

    def render(self):
        """
        Render this Stylesheet object to a string of CSS.
        """
        css_accumulator = []

        for selector in self.definitions.selector_order:
            properties = self.definitions.rules[selector]
            comment = properties.pop("__COMMENT__")

            rendered_properties = "\n".join(
                [self._render_css_item(attr, val) for attr, val in properties.items()]
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
