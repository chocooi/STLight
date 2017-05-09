from django import template
register = template.Library()


@register.filter(name='index')
def index(List, i):
    return List[int(i-1)]

@register.filter
def filter(value):
    return "foo"
