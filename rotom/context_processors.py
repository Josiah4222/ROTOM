from .models import NavbarPattern, SiteContent


def navbar_pattern(request):
    """
    Context processor to make the active navbar pattern and navbar content
    available to all templates automatically.
    """
    try:
        active_pattern = NavbarPattern.objects.filter(is_active=True).first()
    except Exception:
        active_pattern = None

    try:
        navbar_content = {obj.key: obj.value for obj in SiteContent.objects.filter(page='navbar')}
    except Exception:
        navbar_content = {}

    return {
        'navbar_pattern': active_pattern,
        'navbar_content': navbar_content,
    }
