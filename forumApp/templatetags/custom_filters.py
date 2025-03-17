from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retrieve a value from a dictionary in Django templates."""
    return dictionary.get(key, key)  # Return key itself if not found
