# Settings for production environment
from .common import *

# Never run in debug mode
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ()

# TODO: databases config using dj-database-url

# Email
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_HOST = os.environ.get('EMAIL_HOST')

# Mailman list
MAILMAN_LIST_NAME = os.environ.get('MAILMAN_LIST_NAME')
MAILMAN_LIST_PASSWORD = os.environ.get('MAILMAN_LIST_PASSWORD')
MAILMAN_LIST_EMAIL = os.environ.get("MAILMAN_LIST_EMAIL")
MAILMAN_MAIN_URL = os.environ.get('MAILMAN_MAIN_URL')
MAILMAN_ENCODING = os.environ.get('MAILMAN_ENCODING')

# Static files
STATIC_ROOT = os.environ.get('STATIC_ROOT')
STATIC_URL = os.environ.get('STATIC_URL')

SECRET_KET = os.environ.get('SECRET_KEY')
