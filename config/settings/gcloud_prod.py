from .prod import *
import pymysql

pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '/cloudsql/rapid-league-302721:us-east1:my-sql-db',
        'USER': 'django',
        'PASSWORD': 'cs3',
        'NAME': 'django_data_2'
    }
}
