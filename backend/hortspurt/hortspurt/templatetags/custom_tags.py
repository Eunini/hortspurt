from django import template
from datetime import date as datetime_date
register = template.Library()

@register.filter
def has_field(obj, field_name):
    return hasattr(obj, field_name)

@register.filter
def is_today(value):
    return value.date() == datetime_date.today() if hasattr(value, 'date') else value == datetime_date.today()