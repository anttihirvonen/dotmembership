# Settings for production environment
from .common import *

import dj_database_url

# Never run in debug mode
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ()

# Load database configuration from DATABASE_URL
DATABASES = {
    'default': dj_database_url.config()
}

# Email
SERVER_EMAIL = os.environ['SERVER_EMAIL']
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_HOST = os.environ['EMAIL_HOST']

# Mailman list
MAILMAN_LIST_NAME = os.environ['MAILMAN_LIST_NAME']
MAILMAN_LIST_PASSWORD = os.environ['MAILMAN_LIST_PASSWORD']
MAILMAN_LIST_EMAIL = os.environ['MAILMAN_LIST_EMAIL']
MAILMAN_MAIN_URL = os.environ['MAILMAN_MAIN_URL']
MAILMAN_ENCODING = os.environ['MAILMAN_ENCODING']

USE_X_FORWARDED_HOST = True
FORCE_SCRIPT_NAME = '/register'

# Static files are collected and served locally
STATIC_ROOT = os.environ['STATIC_ROOT']
STATIC_URL = os.environ['STATIC_URL']

SECRET_KET = os.environ['SECRET_KEY']
