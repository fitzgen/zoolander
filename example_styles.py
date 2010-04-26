from zoolander import *

sheet = Stylesheet()

with sheet.definitions as rule:
    rule("body",
         font_face="Helvetica, sans-serif",
         line_height=2)

    rule("h1",
         font_size="3em",
         font_weight="bold")

    # Since this is pure Python code, we can use all of Python's control
    # structures, simplest of which are variables.

    SIDE_PANEL_BG_COLOR = "#AACCCC"

    rule("#side-panel",
         background_color=SIDE_PANEL_BG_COLOR)

    # Use dictionaries to mix in sets of properties to multiple rules.

    toolbar_mixin = dict(background_color="#556677",
                         float="left",
                         margin="1em")

    rule("#toolbar li",
         color="#005599",
         font_style="italic",
         **toolbar_mixin)

    rule("#toolbar img",
         border="1px solid #000000",
         **toolbar_mixin)


if __name__ == "__main__":
    print sheet.render()
    sheet.render_to_file(__file__.replace(".py", ".css"))
