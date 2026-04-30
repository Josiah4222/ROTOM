"""
WSGI config for REACHONEETH project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')

application = get_wsgi_application()

# Wrap application to inject SCRIPT_NAME into WSGI environ
_application = application

def application(environ, start_response):
    script_name = os.environ.get('SCRIPT_NAME', '')
    if script_name:
        environ['SCRIPT_NAME'] = script_name
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith(script_name):
            environ['PATH_INFO'] = path_info[len(script_name):]
    return _application(environ, start_response)
