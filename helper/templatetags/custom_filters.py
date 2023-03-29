import json
from django import template
from django.utils import formats
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='split')
def split(value, sep=','):
    return value.split(sep)

@register.filter(name='first')
def first(value):
    return value[0]

@register.filter
def json_loads(value):
    """Converts a JSON string to a Python object."""
    return json.loads(value)

@register.filter(name='naira')
def naira(value):
    """
    Formats the given integer or float value with a naira sign and commas separating thousands, preserving 2 decimal places.
    """
    formatted_value = formats.number_format(value, decimal_pos=2, use_l10n=True)
    formatted_value = intcomma(formatted_value)
    return "₦{0}".format(formatted_value)

