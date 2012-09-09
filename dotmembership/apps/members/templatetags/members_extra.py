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
