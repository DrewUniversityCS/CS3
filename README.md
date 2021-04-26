<img src="https://github.com/DrewUniversityCS/CS3/blob/main/static/images/cs3_text_logo.svg" width="240" height="180">  

# CS3: ComputerScience CapStone CourseScheduler

Capstone project by Aaron, David, Luke and Mahmoud
----
## Large Scale Overview

System Design:

![System Design Diagram](https://github.com/DrewUniversityCS/CS3/blob/main/documentation_diagrams/SystemDesign.png)

Database Relational Schema:

![Database Relational Schema](https://github.com/DrewUniversityCS/CS3/blob/main/documentation_diagrams/relational_schema_final.png)

## 📖 Installation
The app can be installed via Pip or Pipenv depending upon your setup.

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
# Prepare the database (the command will run all the migrations and create an admin with the following credentials: email: admin@gmail.com pwd: 123)
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

## Coding style

### Python

PEP 8 applies to all python code. Read more about it [here](https://www.python.org/dev/peps/pep-0008/).</br>
Below are some essential python style tips:</br>

- CamelCase for class names, snake_case for basically everything else </br>
- Keep things as obvious as possible - don't make acronyms unless you absolutely have to, write explicit variable names e.t.c.</br>
- DRY (don't repeat yourself) is essential. If you need to write the same code twice, you can probably just refactor and avoid doing so.</br>
- Speaking of refactoring - do it often, and carefully. Since this is a volunteer sustained project, there will always be engineers cycling through so keeping the code base accessible and clear is one of, if not the, most important parts of the development process.</br>
- In relation to above, try and document any major decisions you make in the meta data files (i.e devblog.txt). The more of the development history is documented, the easier it will be for those who work on your code next.

When in doubt, refer to *The Zen of Python*, by Tim Peters:
```
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
```

### HTML & CSS

Refer to the [Google HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html).

### JavaScript

Check out the [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html).

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
