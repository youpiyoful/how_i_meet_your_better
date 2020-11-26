from .base import INSTALLED_APPS, MIDDLEWARE
import django_heroku
# import os

# DEBUG = False

ALLOWED_HOSTS = ['45.92.108.117']
django_heroku.settings(locals())


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'himyb',
#         'USER': 'youpiyoful',
#         'PASSWORD': 12345,
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }
