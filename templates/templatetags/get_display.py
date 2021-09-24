from django import template
from common.choices import measurement_type_choices


register = template.Library()


@register.filter
def no_decimals(q):
    str_q = str(q)
    if ".00" in str_q:
        return str_q.replace(".00", "")

    return q


@register.filter
def measurement_type_display(q):
    for choice in measurement_type_choices:
        if choice[0] == q:
            return choice[1]
    return ''

