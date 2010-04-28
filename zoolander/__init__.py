"""
Zoolander - A Python DSL for generating Cascading Style Sheets.
"""
import traceback as tb

_CSS_TEMPLATE = """\
%s
%s {
%s
}"""

right = "right"
left = "left"

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
