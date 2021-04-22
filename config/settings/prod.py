from .base import *
import django_heroku

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

django_heroku.settings(locals())
