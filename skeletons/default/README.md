![Travis](https://travis-ci.org/ARLahan/Flask-Skeleton.svg "Travis")
# Welcome to your new project     
## How to install and use Flask-Skeleton:

  - Clone this repository:
    - git clone https://github.com/ARLahan/Flask-Skeleton.git your_app_name
  - Create a python virtual environment (virtualenv)
  - Activate the virtualenv
  - Install the dependencies:
    - pip install -r requirements.txt
  - Follow the next steps below

## Quick Start


### Install the dependencies

  ```sh
    $ pip install -r requirements.txt
  ```

### Create the database and the admin user:

```sh
  $ export APP_CONFIG="project.config.DevelopmentConfig"

  $ python manage.py create_db

  $ python manage.py db init

  $ python manage.py db migrate

  $ python manage.py create_admin

  $ python manage.py create_data
```

### Run the application

```sh
  $ ./run [-c dev|test|pro]
```
The optional parameters are:
   - ``` -c dev```      for running with development configuration
   - ``` -c test```     for running with testing configuration
   - ``` -c pro```      for running with production configuration


### Testing the application

 * Without coverage:

    ```sh
    $ python manage.py test
    ```

 * With coverage:

    ```sh
    $ python manage.py cov
    ```

## Note

This skeleton is inspired on
RealPython's [https://github.com/realpython/flask-scaffold],
but has some improvements, such as:

  * Relative imports

  * Basic localization

  * The new project has two basic blueprints/packages
    (main and user) which have:
   - Their own static folder
   - Their own templates folder
   - Their own views
   - Their own models
   - Their own forms

  * It runs under Python 2.7+ and 3.3+ (including 3.5)

  * It has been tested (and passed) with the following dependencies:

     - alembic==0.8.3
     - Babel==2.1.1
     - coverage==4.0.2
     - Flask==0.10.1
     - Flask-Babel==0.9
     - Flask-Bcrypt==0.6.2
     - Flask-Bootstrap==3.3.5.7
     - Flask-DebugToolbar==0.10.0
     - Flask-Login==0.3.2
     - Flask-Migrate==1.6.0
     - Flask-Script==2.0.5
     - Flask-SQLAlchemy==2.1
     - Flask-Testing==0.4.2
     - Flask-WTF==0.12
     - Jinja2==2.8
     - SQLAlchemy==1.0.9
     - Werkzeug==0.11.2
     - WTForms==2.0.2

NO LICENCE.
