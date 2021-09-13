from django import template

register = template.Library()


@register.filter()
def pretty(value):
    if "_" in value:
        group_name = value.replace("_", " ").upper()
        return group_name.strip()
    return value.upper()
