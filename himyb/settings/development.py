from .base import *

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ALLOWED_HOSTS = [
    '127.0.0.1',
    'testserver',
]

