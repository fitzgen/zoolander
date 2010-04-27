"""
Zoolander - A Python DSL for generating Cascading Style Sheets.
"""
right = "right"
left = "left"

class _Definitions(object):
    def __init__(self):
        self.rules = {}

    def __enter__(self):
        def rule(selector, **properties):
            """
            Define a CSS rule for "selector" by passing keyword arguments.
            """
            if selector in self.rules:
                self.rules[selector].update(properties)
            else:
                self.rules[selector] = properties
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
        for selector, properties in self.definitions.rules.items():
            rendered_properties = "\n".join(
                ["    %s: %s;" % (key.replace("_", "-"), val)
                 for key, val in properties.items()]
            )
            css_accumulator.append("""\
%s {
%s
}""" % (selector, rendered_properties))

        return "\n\n".join(css_accumulator)

    def render_to_file(self, filename):
        """
        Render this Stylesheet object to a file.
        """
        open(filename, "w").write(self.render())
        return self
