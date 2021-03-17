from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def parse_var(value):
    value = value.replace('_', ' ')
    value = value.capitalize()
    return value
