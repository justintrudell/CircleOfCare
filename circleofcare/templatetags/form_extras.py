from django import template

register = template.Library()

@register.filter(name='field_type')
def text_field(field):
    if "password" in field.name:
        return "password"
    else:
        return "text"

#field.field.widget.__class__.__name__
