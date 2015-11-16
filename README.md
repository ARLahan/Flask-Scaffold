# Another Flask Scaffold

## How to install and use Flask-Scaffold:
  - Clone this repository:
    - git clone https://github.com/ARLahan/Flask-Scaffold.git your_dir_name
  - Create a python virtual environment (virtualenv)
  - Activate the virtualenv
  - Install the dependencies:
    - pip install -r requirements.txt
  - Run scaffold.py as demonstrated bellow

* This scaffold is not a clone but is inspired on the
  RealPython's [https://github.com/realpython/flask-scaffold], but has some improvements, such as:

  * Fully multi-skeleton:
    - Just add a new skeleton to the skeletons directory,
      update scaffold.py with the new skeleton and then run:

      ```sh
      $ python scaffold.py project_name -s skeleton_name [-p full-path/of/the/new/project]
      ```
    - if the -s argument is omitted, the default is chosen.

  * Can install automatically a PYTHON virtual environ (virtualenv)

    ```sh
    $ python scaffold.py project_name -v [-p full-path/of/the/new/project]
    ```

  * Can create automatically a GIT repository

    ```sh
    $ python scaffold.py project_name -g [-p full-path/of/the/new/project]
    ```

  * Can install automatically BOWER single or multiple dependencies

    ```sh
    $ python scaffold.py project_name -b "jquery angular" [-p full-path/of/the/new/project]
    ```

  * Can use all arguments in a unique command line

    ```sh
    $ python scaffold.py project_name -s skeleton_name -g -v -b "jquery angular" [-p full-path/of/the/new/project]
    ```

  * The new project has two basic blueprints (main and user) which have:
   - Their own static folder
   - Their own templates folder
   - Their own views
   - Their own models
   - Their own forms


## Quick Start the new created project

  * Change to the new project root directory and run:

    ```sh
    $ ./run
    ```

### Creating the database and the admin user:

  ```sh
  $ export APP_CONFIG="project.config.DevelopmentConfig"
  $ python manage.py create_db
  $ python manage.py db init
  $ python manage.py db migrate
  $ python manage.py create_admin
  $ python manage.py create_data
  ```

  * You can login into the application using:
    - email: admin@example.com
    - password: admin

### Runnig the application
  * Just type :

    ```sh
    $ ./run [-c dev|test|pro]
    ```

The optional -c parameters to pass can be one of the following:
   - dev   for running with development configuration
   - test  for running with testing configuration
   - pro   for running with production configuration

 If the -c parameter is omitted, the application will run with
 the default configuration, which is -c dev


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

* Both the scaffold and the new project run under Python 2.7+ and 3.3+ (including 3.5)

* It is generated a new project on the fly, with the following
 dependencies installed (if the -v argument is used):
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
