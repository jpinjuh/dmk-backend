# Install

Install instructions for development environments.

## Preparing Python environment

0) Install system dependencies

~~~
$ sudo apt-get install build-essential git python3 python3-venv \
python3-dev libffi-dev postgresql-server-dev-all
~~~

1) prepare Python virtual environment

~~~
git clone ...
cd flask_project
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip pip-tools
deactivate
source .venv/bin/activate
pip-sync requirements.txt
~~~

## External services

### Database

Commands below produce database settings with weak, easy to guess passwords.
Do not use these in production!

0) Install PostgreSQL server

~~~
$ sudo apt-get install postgresql postgresql-contrib
~~~

1) Use PostgreSQL tools to create database

~~~
$ sudo -u postgres psql
postgres=# CREATE ROLE student LOGIN PASSWORD 'student' VALID UNTIL 'infinity';
postgres=# CREATE DATABASE dmk_dev WITH ENCODING='UTF8' OWNER=student CONNECTION LIMIT=-1;
postgres=# CREATE DATABASE dmk_test WITH ENCODING='UTF8' OWNER=student CONNECTION LIMIT=-1;
~~~

2) Edit settings (ie. database URI, secret key, etc...) in `development.conf` (SKIP THIS STEP)

~~~
sqlalchemy_uri = postgresql://student:student@localhost:5432/flask_project_dev
~~~

3) Run database migrations:

~~~
source .venv/bin/activate
python manage.py db upgrade
~~~