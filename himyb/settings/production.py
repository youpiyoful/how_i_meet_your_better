from .base import *
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://f9cdebed656544dba8fdec428470c116@o483455.ingest.sentry.io/5535646",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
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
