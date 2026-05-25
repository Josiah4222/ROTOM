"""
lang_tags.py — Template tag for bilingual EN/AM content switching.

Usage in templates:
    {% load lang_tags %}
    {% bilingual story.title story.title_am %}

Renders:
    <span class="lang-en">English text</span>
    <span class="lang-am">Amharic text</span>   ← only if am value is non-empty

The CSS in base.html hides/shows the right span based on [data-lang] on <html>.
"""

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def bilingual(en_value, am_value='', tag='span', **kwargs):
    """
    Render a bilingual element.
    If am_value is empty, renders only the EN span (no switching needed).
    """
    en_text = conditional_escape(en_value) if en_value else ''
    am_text = conditional_escape(am_value) if am_value else ''

    if not am_text:
        # No translation — just output the value directly, no wrapper needed
        return mark_safe(en_text)

    return mark_safe(
        f'<{tag} class="lang-en">{en_text}</{tag}>'
        f'<{tag} class="lang-am">{am_text}</{tag}>'
    )


@register.simple_tag
def bilingual_block(en_value, am_value=''):
    """
    Same as bilingual but uses <span> with display:block for multi-line text
    like paragraphs where you don't want inline elements.
    """
    return bilingual(en_value, am_value, tag='span')
