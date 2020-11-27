from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'himyb',
        'USER': 'postgresql',
        'PASSWORD': 12345,
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
