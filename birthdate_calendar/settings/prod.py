from .base import *

DEBUG = False

ENVIRONMENT_NAME = 'Production'
ENVIRONMENT_COLOR = '#b21c17'

ALLOWED_HOSTS = ['loan-cb.fr', 'birthdates.loan-cb.fr']

CORS_ALLOWED_ORIGINS = [
    'https://loan-cb.fr',
    'https://birthdates.loan-cb.fr',
]

STATIC_URL = 'https://loan-cb.fr/birthdate_calendar/'
STATIC_ROOT = '/home/colo0019/public_html/birthdate_calendar/'
