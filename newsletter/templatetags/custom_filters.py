from django import template
import re

register = template.Library()

@register.filter
def truncatehtmlwords(value, arg):
    """
    Truncate HTML content to a specified number of words.
    """
    if not value:
        return ""
    
    # Remove HTML tags
    value = re.sub(r'<[^>]+>', '', value)
    words = value.split()
    
    # Truncate to the specified number of words
    if len(words) > arg:
        return ' '.join(words[:arg]) + '...'
    return value
