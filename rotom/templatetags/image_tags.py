import os
from django import template
from django.conf import settings
from django.templatetags.static import static

from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def webp_picture(image_path, alt="", img_class="", loading="lazy", width=None, height=None, fetchpriority="auto", style=""):
    """
    Renders a <picture> tag with WebP source and fallback.
    Usage: {% webp_picture 'images/photo.jpg' alt="Description" img_class="my-img" %}
    """
    if not image_path:
        return ""

    # Ensure image_path is a string
    image_path_str = str(image_path)

    # Handle both static paths and media URLs
    # If it starts with http, /media/, or media/, it's a media/external URL
    is_static = not (image_path_str.startswith('http') or 
                    image_path_str.startswith('/media/') or 
                    image_path_str.startswith('media/'))
    
    if is_static:
        # Clean path if it starts with /static/
        if image_path_str.startswith('/static/'):
            image_path_str = image_path_str[8:]
        elif image_path_str.startswith('static/'):
            image_path_str = image_path_str[7:]
            
        base_path = image_path_str.rsplit('.', 1)[0]
        webp_url = static(f"{base_path}.webp")
        fallback_url = static(image_path_str)
    else:
        # For media files
        if image_path_str.lower().endswith('.webp'):
            # Already webp, no need for <picture> source
            img_attrs = f'src="{image_path_str}" alt="{alt}" class="{img_class}" loading="{loading}" decoding="async"'
            if width: img_attrs += f' width="{width}"'
            if height: img_attrs += f' height="{height}"'
            if style: img_attrs += f' style="{style}"'
            if fetchpriority != "auto": img_attrs += f' fetchpriority="{fetchpriority}"'
            return mark_safe(f'<img {img_attrs}>')
        
        base_path = image_path_str.rsplit('.', 1)[0]
        webp_url = f"{base_path}.webp"
        fallback_url = image_path_str

    # Build the attributes string
    img_attrs = f'src="{fallback_url}" alt="{alt}" class="{img_class}" loading="{loading}" decoding="async"'
    if width: img_attrs += f' width="{width}"'
    if height: img_attrs += f' height="{height}"'
    if style: img_attrs += f' style="{style}"'
    if fetchpriority != "auto": img_attrs += f' fetchpriority="{fetchpriority}"'

    html = f'<picture><source srcset="{webp_url}" type="image/webp"><img {img_attrs}></picture>'
    return mark_safe(html)
