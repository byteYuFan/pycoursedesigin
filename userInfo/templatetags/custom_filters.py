# custom_filters.py

from django import template

register = template.Library()


@register.filter
def divide(value, divisor):
    return round(int(value) / divisor, 2)
