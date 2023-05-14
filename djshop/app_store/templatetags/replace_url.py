from django import template

register = template.Library()


@register.filter
def replace_url(value):
    return value.replace("/", "%")
