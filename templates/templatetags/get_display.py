from django import template


register = template.Library()


@register.filter
def no_decimals(q):
    str_q = str(q)
    if ".00" in str_q:
        return str_q.replace(".00", "")

    return q


# @register.filter
# def item_types_display(q):
#     for choice in categories:
#         if choice[0] == q:
#             return choice[1]
#     return ''
