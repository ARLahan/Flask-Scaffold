# Welcome to your project

## How to install and use Flask-Scaffold:
  - Clone this repository:
    - git clone https://github.com/ARLahan/Flask-Scaffold.git
  - Create a python virtual environment (virtualenv)
  - Activate the virtualenv
  - Install the dependencies:
    - pip install -r requirements.txt
  - Run scaffold.py as demonstrated bellow

  * This project has two basic blueprints (main and user) which have:
   - Their own static folder
   - Their own templates folder
   - Their own views
   - Their own models
   - Their own forms


## Quick Start the new created project
### Create the database and the admin user:

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_admin
$ python manage.py create_data
```

### Running the application
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
