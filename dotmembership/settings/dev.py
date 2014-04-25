# Settings only to be used for development
from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()
MANAGERS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dotmembership.db'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

MAILMAN_LIST_NAME = ""
MAILMAN_LIST_PASSWORD = ""
MAILMAN_LIST_EMAIL = ""
MAILMAN_MAIN_URL = ""
MAILMAN_ENCODING = ""

# This can be used in tests to verify that all variables
# were rendered correctly.
TEMPLATE_STRING_IF_INVALID = "[INVALID VAR]"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'development secret key'

# Install debug toolbar
INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS' : False}
INTERNAL_IPS = ('127.0.0.1', '192.168.1.7')
