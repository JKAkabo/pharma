import django_heroku
from .base import *

DEBUG = True

django_heroku.settings(locals())
