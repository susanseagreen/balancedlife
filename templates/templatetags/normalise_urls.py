from django import template

register = template.Library()


@register.filter()
def normalise(value):
    group = value.strip()
    return group.replace(" ", "_")
