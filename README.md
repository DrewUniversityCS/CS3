<img src="https://github.com/DrewUniversityCS/CS3/blob/main/static/images/cs3_text_logo.png" width="240" height="180">  

Capstone project by Aaron, David, Luke and Mahmoud
----

## 📖 Installation
The app can be installed via Pip or Pipenv depending upon your setup.


### Pip

```
$ python3 -m venv csrs
$ source csrs/bin/activate
$ pip install -r requirements.txt
$ python manage.py prepdb
$ python manage.py runserver
# Load the site at http://127.0.0.1:8000
```

### Pipenv

```
$ pipenv install
$ pipenv shell
$ python manage.py prepdb
$ python manage.py runserver
# Load the site at http://127.0.0.1:8000
```

## Setup

```
# Run migrations, install fixtures and create test admin (email: admin@gmail.com pwd: 123)
$ python manage.py prepdb

# Run a command to install all necessary dependencies for tailwind css
$ python manage.py tailwind install

# Start tailwind in dev mode
$ python manage.py tailwind start

# Confirm everything is working:
$ python manage.py runserver

# Load the site at http://127.0.0.1:8000
```

----

## License

[The MIT License](LICENSE)

<!-- ## Next Steps

- Use [PostgreSQL locally via Docker](https://wsvincent.com/django-docker-postgresql/)
- Use [django-environ](https://github.com/joke2k/django-environ) for environment variables
- Update [EMAIL_BACKEND](https://docs.djangoproject.com/en/3.0/topics/email/#module-django.core.mail) to configure an SMTP backend
- Make the [admin more secure](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure)

## Adding Social Authentication

- [Configuring Google](https://wsvincent.com/django-allauth-tutorial-custom-user-model/#google-credentials)
- [Configuring Facebook](http://www.sarahhagstrom.com/2013/09/the-missing-django-allauth-tutorial/#Create_and_configure_a_Facebook_app)
- [Configuring Github](https://wsvincent.com/django-allauth-tutorial/)
- `django-allauth` supports [many, many other providers in the official docs](https://django-allauth.readthedocs.io/en/latest/providers.html) -->
