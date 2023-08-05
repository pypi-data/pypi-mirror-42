from django import template

from django.conf import settings

register = template.Library()


@register.filter
def from_firebase_settings(key):
    try:
        return settings.FIREBASE[key]
    except KeyError:
        return ''
