from django import template
from jdatetime import datetime as jdatetime_datetime

register = template.Library()

@register.filter
def jalali_datetime(value, format_string="%Y:%m:%d - %H:%M:%S"):
    """Convert a Django jDateTimeField to a formatted Jalali datetime string."""
    if not value:
        return ""

    if isinstance(value, str):
        return value  # Return as is if already formatted

    jalali_date = jdatetime_datetime.fromgregorian(datetime=value)
    return jalali_date.strftime(format_string)
