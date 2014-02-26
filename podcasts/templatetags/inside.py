from django import template

register = template.Library()

@register.filter()
def inside(value, collection):
    return value in collection if isinstance(collection, list) else False