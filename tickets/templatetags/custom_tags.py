from django import template
from django.utils import formats
import datetime
from django.contrib.humanize.templatetags import humanize
register = template.Library()

@register.filter(expects_localtime=True, is_safe=False)
def custom_date(value, arg=None):
    if value in (None, ''):
        return ''

    if isinstance(value, str):
        api_date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        value = datetime.datetime.strptime(value, api_date_format)

    try:
        return humanize.naturaltime(value)
    except AttributeError:
        try:
            print(type(format(value, arg)))
            return format(value, arg)
        except AttributeError:
            return ''
