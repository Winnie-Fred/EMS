import json
from django import template

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
