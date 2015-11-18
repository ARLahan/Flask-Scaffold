# Another Flask Scaffold
## How to install and use Flask-Scaffold:
========================================
  - Clone this repository:
    - git clone https://github.com/ARLahan/Flask-Scaffold.git your_dir_name
  - Create a python virtual environment (virtualenv)
  - Activate the virtualenv
  - Install the dependencies:
    - pip install -r requirements.txt
  - Run scaffold.py as demonstrated bellow

* This scaffold is not a clone but is inspired on the
  RealPython's [https://github.com/realpython/flask-scaffold],
  but has some improvements, such as:

  * Relative imports

  * Fully multi-skeleton:
    - Just add a new skeleton to the skeletons directory and automatically
      scaffold.py will find them

  * Detects which pythons versions are installed and let you choose each one
    to use

  * Python 2.7 and 3.3+ (including 3.5)

  * You may use bower to install dependencies to your project, using
    -b "package1 package2 ..."

  * Automatically install a virtualenv and python dependencies
    if you choose to use the -v parameter giving you the choice
    to install any of the python versions you have in your system

  * Initiates a git repository at the project's root path, if you use the
    the -g parameter

  * You choose where to install the new project using the -p parameter,
    although it defaults to the user's home directory if the -p
    parameter is omitted

## Examples
===========
### Installing without parameters

  ```sh
      $ python scaffold.py project_name
  ```

  Creates a new project <project_name> at user's home directory without
  any dependencies, virtualenv, bower or git

### Installing with virtualenv

  ```sh
    $ python scaffold.py project_name -v 2.7
  ```

  Creates a new project with python 2.7 and virtualenv with all the project's
  dependencies installed through requirements.txt

### Installing with git

  ```sh
    $ python scaffold.py project_name -v 3.5 -g
  ```

  Creates a new project with python 3.5 and virtualenv and initiates a git
  repository at the projectŝ root directory

### Installing with bower

  ```sh
    $ python scaffold.py project_name -b "jquery angular"
  ```

  Creates a new project and installs JQuery and Angularjs in the static folder

### Installing with all parameters

  ```sh
    $ python scaffold.py project_name -s skeleton_name -g -v 2.7 -b "jquery angular" [-p full-path/of/the/new/project]
  ```



NO LICENCE.
