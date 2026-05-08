from .models import NavbarPattern


def navbar_pattern(request):
    """
    Context processor to make the active navbar pattern available to all templates.
    """
    try:
        active_pattern = NavbarPattern.objects.filter(is_active=True).first()
        return {'navbar_pattern': active_pattern}
    except Exception:
        return {'navbar_pattern': None}
