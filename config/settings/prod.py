from .base import *

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '/cloudsql/rapid-league-302721:us-east1:my-sql-db',
        'USER': 'django',
        'PASSWORD': 'drewLovesSquirrels21',
        'NAME': 'django_data'
    }
}
