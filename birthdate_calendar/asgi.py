"""
ASGI config for birthdate_calendar project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    f'birthdate_calendar.settings.{"dev" if os.getenv("PY_ENV") == "dev" else "prod"}'
)

application = get_asgi_application()
