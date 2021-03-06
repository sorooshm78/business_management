from django import template

register = template.Library()


@register.filter()
def percent(value, arg):
    if arg != 0:
        return round((value / arg) * 100, 2)
    return None
