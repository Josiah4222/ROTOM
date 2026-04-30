class ScriptNameMiddleware:
    """Injects SCRIPT_NAME into every request so {% url %} tags include the prefix."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        script_name = getattr(settings, 'FORCE_SCRIPT_NAME', '')
        if script_name:
            request.META['SCRIPT_NAME'] = script_name
        return self.get_response(request)
