from django import template
from common.choices import categories

register = template.Library()


@register.filter
def item_types_display(q):
    for choice in categories:
        if choice[0] == q:
            return choice[1]
    return ''


@register.filter
def item_types_svg(q):
    for choice in categories:
        if choice[0] == q:
            return choice[2]
    return ''
