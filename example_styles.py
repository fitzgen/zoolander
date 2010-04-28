from zoolander import *

sheet = Stylesheet()

with sheet.definitions as rule:

    # Zoolander's semantics map directly to CSS, nothing new here.

    rule("body",
         font_face="Helvetica, sans-serif",
         line_height=2)

    rule("h1",
         font_size=em(3),
         font_weight=bold)

    # Since this is pure Python code, we can use all of Python's control
    # structures, simplest of which are variables and arithmetic operators.

    side_panel_bg_color = "#AACCCC"
    spacing = em(2)

    rule("#side-panel",
         margin=spacing/2,
         padding=spacing+1,
         background_color=side_panel_bg_color)

    # Use dictionaries to mix in sets of properties to multiple rules.

    toolbar_mixin = dict(background_color="#556677",
                         float="left",
                         margin=em(1))

    rule("#toolbar li",
         color="#005599",
         font_style=italic,
         **toolbar_mixin)

    rule("#toolbar img",
         border="1px solid #000000",
         **toolbar_mixin)


if __name__ == "__main__":
    print sheet.render()
