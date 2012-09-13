from django.utils.safestring import mark_safe
from django import template
register = template.Library()


@register.filter
def getfield(model, field):
    """
    Helper to get model field value dynamically.
    """
    return getattr(model, field, "")


@register.filter
def getfieldname(model, field):
    """
    Helper to get model field value dynamically.
    """
    return model._meta.get_field(field).verbose_name


@register.inclusion_tag('members/div_datarow.html')
def print_row(th, td, extra_td=""):
    return {'th': th, 'td': mark_safe(u"%s%s" % (td, extra_td))}
