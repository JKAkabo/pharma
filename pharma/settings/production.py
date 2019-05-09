import django_heroku

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['localhost']

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
