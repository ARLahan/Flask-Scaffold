# Another Flask Skeleton

This skeleton is based on RealPython's [https://github.com/realpython/flask-scaffold],
but has some improvements, such as:

 * Relative imports

 * Each of the two basic blueprints (main and user) have:
   - Their own static folder
   - Their own templates folder
   - Their own views
   - Their own models
   - Their own forms

 * It runs under Python 2.7+ and 3.3+ (including 3.5)

 * It has been tested (and passed) with the following dependencies:
    - alembic==0.8.3
    - blinker==1.4
    - coverage==4.0.2
    - dominate==2.1.16
    - Flask==0.10.1
    - Flask-Bcrypt==0.6.2
    - Flask-Bootstrap==3.3.5.7
    - Flask-DebugToolbar==0.10.0
    - Flask-Login==0.3.2
    - Flask-Migrate==1.6.0
    - Flask-Script==2.0.5
    - Flask-SQLAlchemy==2.1
    - Flask-Testing==0.4.2
    - Flask-WTF==0.12
    - itsdangerous==0.24
    - Jinja2==2.8
    - Mako==1.0.3
    - MarkupSafe==0.23
    - python-bcrypt==0.3.1
    - python-editor==0.4
    - SQLAlchemy==1.0.9
    - visitor==0.1.2
    - Werkzeug==0.11.2
    - WTForms==2.0.2


## Quick Start

Update the SECRET_KEY in config.py, and then run:
```sh
$ ./run
```

### Creating the database and the admin user:

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
```

### Runnig the application
Just type :

```sh
$ ./run [-c dev|test|pro]
```
The optional parameters are:
   - -c dev   for running with development configuration
   - -c test  for running with testing configuration
   - -c pro   for running with production configuration


### Testing the application

 * Without coverage:

```sh
$ python manage.py test
```

 * With coverage:

```sh
$ python manage.py cov
```
