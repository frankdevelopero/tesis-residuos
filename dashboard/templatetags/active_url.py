from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    """
    Devuelve 'active' si el nombre de la URL coincide con el URL actual.
    """
    request = context['request']
    if request.resolver_match.url_name == url_name:
        return 'active'
    return ''
