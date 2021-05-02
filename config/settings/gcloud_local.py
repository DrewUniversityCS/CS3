from .base import *

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = '43)%4yx)aa@a=+_c(fn&kf3g29xax+=+a&key9i=!98zyim=8j'

import pymysql

pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'django',
        'PASSWORD': 'cs3',
        'NAME': 'django_data_2',
    }
}

"""
To run the proxy:
cloud_sql_proxy.exe -instances="rapid-league-302721:us-east1:my-sql-db"=tcp:3306

dont forget to change manage.py settings to this file
"""