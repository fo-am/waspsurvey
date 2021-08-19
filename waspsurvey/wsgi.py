"""
WSGI config for waspsurvey project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "waspsurvey.settings")
sys.path.append('/var/www/waspsurvey/')

activator = '/home/dave/code/waspsurvey/.venv/bin/activate_this.py'  # Looted from virtualenv; should not require modification, since it's defined relatively
with open(activator) as f:
    exec(f.read(), {'__file__': activator})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
