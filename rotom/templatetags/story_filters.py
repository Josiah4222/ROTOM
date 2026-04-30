from django import template

register = template.Library()

@register.filter(name='split_paragraphs')
def split_paragraphs(value):
    """Split content into paragraphs by double newlines"""
    if not value:
        return []
    # Split by double newlines and filter out empty strings
    paragraphs = [p.strip() for p in value.split('\n\n') if p.strip()]
    return paragraphs
