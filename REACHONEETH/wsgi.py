"""
WSGI config for REACHONEETH project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')

_application = get_wsgi_application()

def application(environ, start_response):
    from django.conf import settings
    script_name = getattr(settings, 'FORCE_SCRIPT_NAME', '') or ''
    if script_name:
        environ['SCRIPT_NAME'] = script_name
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith(script_name):
            environ['PATH_INFO'] = path_info[len(script_name):]
    return _application(environ, start_response)
