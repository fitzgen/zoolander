"""
Zoolander - A Python DSL for generating Cascading Style Sheets.
"""
import traceback as tb
from units import *

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

            def render_css_item(attr, val):
                """
                Render a single key/val pair.
                """
                attr = attr.replace("_", "-")
                return "    %s: %s" % (attr, val)

            rendered_properties = "\n".join(
                [render_css_item(attr, val) for attr, val in properties.items()]
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
