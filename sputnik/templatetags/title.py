from django import template

register = template.Library()


@register.tag
def title(parser, token):
    """
    Create a title string.

    It's used in the following way:

        {% title "About" user.username "Lol" %}

    Which would produce the string: "Lol - matachi - About - PodFlare.com"
    """
    args = token.split_contents()
    values = [parser.compile_filter(arg) for arg in args[1:]]
    return TitleNode(values)


class TitleNode(template.Node):
    def __init__(self, titles):
        self.titles = titles
        self.titles.reverse()

    def render(self, context):
        return "{} - {}".format(
            " - ".join(t.resolve(context) for t in self.titles),
            "PodFlare.com"
        )
