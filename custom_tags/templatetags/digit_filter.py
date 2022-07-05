from django import template

register = template.Library()


@register.filter()
def number_format(value):
    return "{:,}".format(value)
