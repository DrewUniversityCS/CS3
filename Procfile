web: gunicorn config.wsgi --log-file -
release: python manage.py prepdb
release: bin/run_cloud_sql_proxy