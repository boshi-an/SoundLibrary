"""
WSGI config for SoundLib project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from SoundLib import settings

settings.DEBUG = False
settings.SITE_URL = settings.SITE_URL_DEPLOY
settings.STATIC_ROOT = os.path.join(settings.BASE_DIR, 'Static')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SoundLib.settings')

application = get_wsgi_application()