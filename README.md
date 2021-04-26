<br />
<p align="center">
  <a href="https://github.com/DrewUniversityCS/CS3">
    <img src="https://github.com/DrewUniversityCS/CS3/blob/main/static/images/cs3_text_logo.svg" alt="Logo" width="249" height="180">
  </a>
</p> 

# CS3: Computer Science CapStone Course Scheduler
### Capstone project by Aaron, David, Luke and Mahmoud

<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#problem-statement">Problem Statement</a></li>
      </ul>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
       <ul>
        <li><a href="#large-scale-overview">Large Scale Overview</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
      <ul>
        <li><a href="#coding-style">Coding Style</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## Problem Statement

CS3 was originally built for the head of Drew University's Math & CS department, Sarah Abramowitz, to facilitate the process of scheduling college courses and managing the data generated in the process. The application provides a robust interface for managing scheduling data, rendering it in a clear fashion and storing it offline in the csv format.

## Built With

### Backend
- Django
- Django-allauth
- Whitenoise
- Gunicorn
- Heroku and GCP for deployment

### Frontend
- Crispy Forms
- TailwindCSS
- FontAwesome
- HeroPatterns
- HeroIcons
- django_tailwind for easy django integration for tailwind
- crispy_tailwind for applying tailwind styles to crispy forms

## Large Scale Overview

System Design:

![System Design Diagram](https://github.com/DrewUniversityCS/CS3/blob/main/documentation_diagrams/SystemDesign.png)

Database Relational Schema:

![Database Relational Schema](https://github.com/DrewUniversityCS/CS3/blob/main/documentation_diagrams/relational_schema_final.png)

## Installation
The app can be installed via Pip or Pipenv depending upon your setup.

### Pipenv

```
$ pipenv install
$ pipenv shell
$ python manage.py prepdb
$ python manage.py runserver
# Load the site at http://127.0.0.1:8000
```

### Setup

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

## License

[The MIT License](LICENSE)

