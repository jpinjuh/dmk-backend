<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Description](#description)
- [Installation](#installation)
- [Running](#running)
	- [Starting dev server](#starting-dev-server)
	- [Dependencies maintenance](#dependencies-maintenance)
	- [Seeding database with fake development data](#seeding-database-with-fake-development-data)
	- [Application shell](#application-shell)
- [...](#)
	- [Application routes](#application-routes)

<!-- /TOC -->

# Description

Example Flask application with:
    - SQLAlchemy + PostgreSQL model layer

Used as a teaching tool.

# Installation

See [INSTALL.md](INSTALL.md)

# Running

## Starting dev server

~~~
source .venv/bin/activate
python manage.py runserver
~~~

## Dependencies maintenance

Add/remove packages from `requirements.in` and then:

~~~
source .venv/bin/activate
pip-compile requirements.in
pip install -r requirements.txt
~~~

## Seeding database with fake development data

~~~
source .venv/bin/activate
python manage.py db truncate && python manage.py db upgrade && python manage.py db seed
~~~

Note that `seed` might sometimes fail on unique constraint violation. This is normal, just re-run above code until it passes

## Application shell

~~~
python manage.py shell
python code....
# ...
~~~

## Application routes

~~~
source .venv/bin/activate
python manage.py routes
~~~
