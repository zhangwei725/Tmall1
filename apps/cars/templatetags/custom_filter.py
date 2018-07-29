from django import template

register = template.Library()


# value|过滤器的名称:参数
@register.filter
def multiply(value, params):
    return value * params
