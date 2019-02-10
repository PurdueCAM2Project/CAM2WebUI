from django import template
from django.apps import apps

register = template.Library()


@register.filter(name='modulo')
def modulo(value, arg):
    return value % arg
