from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    """Template filter to get dynamic attribute of an object"""
    return getattr(obj, attr_name, None)
