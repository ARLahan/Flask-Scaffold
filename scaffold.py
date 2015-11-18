#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Al-Rama Lahan <lahangit@gmail.com>.
# NOLICENCE.
"""
Create a new project from a given scaffolding a project skeleton.

Multi-skeleton scaffolder.
You just need to:
 - put your application skeletons in the skeletons directory;
 - at the root of your skeleton directory create a file with .prj
   extension, where its name will identify the new project's name;
 - run `python scaffold.py appname -s skeleton_name` -p /path/to/new/project
   if the -s parameter is omitted, scaffold.py will choose the default
   skeleton, which name should be 'default' and should reside at the skeletons
   directory; the -s parameter is limitted by the results of the
   skeletons found, so it is not possible to select a non-existent skeleton;
 - other parameters can be added to scaffold.py such as:
    -v to install a python virtual environment;
    -g to initiate a git repository at te new project's root directory;
    -b "package1 package2 ..." to install the selected bower packages.
    To be able to use the -v -g or -b parameters, git, bower ans pyvenv (for
    python 3.4+) or virtualenv must have been previously installed on the
    system.
"""

import sys
import os
import argparse
import jinja2
import codecs
from subprocess import Popen, PIPE
from shutil import copytree, copyfile, ignore_patterns
import ntpath

if sys.version_info < (3, 0):
    from shutilwhich import which
    input = raw_input
else:
    from shutil import which


# Globals #
cwd = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))
user_home_dir = os.path.expanduser('~')

# Jinja2 environment and location for the templates for scaffolding
template_loader = jinja2.FileSystemLoader(
    searchpath=os.path.join(script_dir, 'templates'))
template_env = jinja2.Environment(loader=template_loader)


def scan_skeletons():
    """Scan skeletons directory for skelettons to scaffold.
    Each skeleton must have at its root directory a filename
    with .prj extension which will identify the name to give
    to the new project.

    When scaffold.py finds the .prj file, adds its name, stripped
    of its extension, to the skeletons dictionary as the pair value
    to the skeleton directory name, which is the key.
    """
    # Defining the app skeletons
    # get a list of installed skeletons
    # as choices to the -s parameter
    skeletons = {}
    os.chdir('skeletons')
    skeletons_list = os.listdir('.')
    # Scanning for skeletons
    for skeleton in skeletons_list:
        project_dir = os.scandir(skeleton)
        for project_file in project_dir:
            # if it is a .prj file
            if project_file.name.endswith('.prj') and project_file.is_file():
                skeletons[skeleton] = project_file.name.split('.')[0]
    # Returns to the original directory
    os.chdir(cwd)
    return skeletons_list, skeletons


def scan_python_versions():
    """Scan for the python versions existing in the system.
    It will limit the choices of python virtual environments to install.

    It is assumed that the python binayries are in /usr/bin although some
    systems have them in /usr/local/bin, or in any other place,
    so we shall get the directory by using `which` to locate
    those existing in the system.
    """
    # start defining a list of python versions we accept
    # and then find those existing in the system
    acceptable_versions = ['python2.7', 'python3.3', 'python3.4', 'python3.5']
    py_versions_found = []
    for py_version in acceptable_versions:
        py_version = which(py_version)
        if py_version:
            # we just need the number version, so we strip the rest
            py_version = ntpath.basename(py_version)[6:]
            py_versions_found.append(py_version)
    return py_versions_found


def get_arguments(argv, skeletons_list, python_versions):
    """Parsing the received arguments from command line.

    The manadtory argument to pass is the new application name,
    although the path for its installation also should be given or
    the new application will be installed in the current working
    directory in a new directory named from the application name.
    """
    parser = argparse.ArgumentParser(description='Scaffold a Flask Skeleton.')
    parser.add_argument('appname',
                        help='The application name.')
    parser.add_argument('-p', '--path',
                        default=user_home_dir,
                        help='The path where the application \
                              will be located. If none, it will \
                              be installed in the user\'s home directory.')
    parser.add_argument('-s', '--skeleton', choices=skeletons_list,
                        default='default',
                        help='The skeleton to use from a given list of choices. \
                        If none, it will choose the default skeleton.')
    parser.add_argument('-b', '--bower',
                        help='Install dependencies via bower. \
                        e.g. syntax: `-b "jquery bootstrap"`')
    parser.add_argument('-v', '--virtualenv', choices=python_versions,
                        default='',
                        help='Install a virtual environment \
                        based on the user\'s choice or, if empty, does not \
                        install any virtual environment.')
    parser.add_argument('-g', '--git', action='store_true',
                        help='Create a git repository for the application.')
    args = parser.parse_args()

    # Variables #
    fullpath = os.path.join(args.path, args.appname) \
        if args.path else os.path.join(cwd, args.appname)
    skeleton = args.skeleton if args.skeleton else 'default'
    # skeleton = [key for key in skeletons.keys() if key == args.skeleton][0]
    skeleton_dir = os.path.join(cwd, 'skeletons', skeleton)

    return args, skeleton, skeleton_dir, fullpath


def generate_brief(args):
    """Context dictionary to pass to the scaffold template.
    This will be used for generate a confirmation screen.
    """
    template_ctx = {
        'pyversion': args.virtualenv,
        'appname': args.appname,
        'bower': args.bower,
        'virtualenv': args.virtualenv,
        'skeleton': args.skeleton,
        'path': args.path if args.path else os.path.join(cwd, args.appname),
        'git': args.git
    }
    template = template_env.get_template('brief.html')
    return template.render(template_ctx)


def make_structure(args, skeleton, skeleton_dir, fullpath):
    """Process the arguments and scaffold the new application."""
    # Copy files and folders
    print('Copying files and folders...')
    copytree(os.path.join(script_dir, skeleton_dir), fullpath,
             ignore=ignore_patterns('*.pyc', '*.prj*'))
    print('Creating the application configuration...')
    secret_key = codecs.encode(os.urandom(64), 'hex').decode('utf-8')
    csrf_secret_key = codecs.encode(os.urandom(64), 'hex').decode('utf-8')
    template_ctx = {
        'secret_key': secret_key,
        'csrf_secret_key': csrf_secret_key,
        'skeleton': skeletons[skeleton],
        'app_name': args.appname,
    }

    # Create manage.py
    try:
        template = template_env.get_template('manage.py.html')
        with open(os.path.join(fullpath, 'manage.py'), 'w') as fd:
            fd.write(template.render(template_ctx))
    except FileNotFoundError:
        pass

    # Create the project config.py files
    try:
        template = template_env.get_template('config.py.html')
        with open(os.path.join(
                fullpath, skeletons[skeleton], 'config.py'), 'w') as fd:
            fd.write(template.render(template_ctx))
    except FileNotFoundError:
        pass


def add_bower(bower, skeleton, fullpath):
    """Install the selected bower dependencies."""
    bower_exe = which('bower')
    if bower_exe:
        os.chdir(os.path.join(fullpath, skeletons[skeleton], 'static'))

        for dependency in bower:
            output, error = Popen(
                [bower_exe, 'install', dependency],
                stdout=PIPE,
                stderr=PIPE
            ).communicate()
            if error:
                print('An error occurred with Bower!')
                print(error)
    else:
        print('Could not find bower. '
              'Ignoring the request for bower '
              'dependencies installation...')


def add_virtualenv(fullpath):
    """Create a python virtual environment named flask."""
    if args.virtualenv == "2.7" or args.virtualenv == "3.3":
        virtualenv_exe = which(''.join(['virtualenv-', args.virtualenv]))
    else:
        virtualenv_exe = which(''.join(['pyvenv-', args.virtualenv]))
    if virtualenv_exe:
        output, error = Popen(
            [virtualenv_exe, os.path.join(fullpath, 'flask')],
            stdout=PIPE,
            stderr=PIPE
        ).communicate()

        if error:
            with open('virtualenv_error.log', 'w') as fd:
                fd.write(error.decode('utf-8'))
                print('An error occurred with virtualenv!')
                sys.exit(2)

        venv_bin = os.path.join(fullpath, 'flask/bin')
        print('Adding application requirements...')
        output, error = Popen(
            [
                os.path.join(venv_bin, 'pip'),
                'install',
                '-r',
                os.path.join(fullpath, 'requirements.txt')
            ],
            stdout=PIPE,
            stderr=PIPE
        ).communicate()
        if error:
            with open('pip_error.log', 'w') as fd:
                fd.write(error.decode('utf-8'))
                sys.exit(2)
    else:
        print('Could not find a valid virtualenv executable. '
              'Ignoring the request for installing a '
              'virtual environment...')


def add_git(fullpath):
    """Create a git repository at the project's root directory."""
    git_exe = which('git')
    if git_exe:
        output, error = Popen(
            ['git', 'init', fullpath],
            stdout=PIPE,
            stderr=PIPE
        ).communicate()

        if error:
            with open('git_error.log', 'w') as fd:
                fd.write(error.decode('utf-8'))
                print('Error with git init!')
                sys.exit(2)
        print('Adding a `.gitignore` file...')
        copyfile(
            os.path.join(script_dir, 'templates', '.gitignore'),
            os.path.join(fullpath, '.gitignore')
        )
    else:
        print('Could not find git. '
              'Ignoring the request for initializing '
              'a `.git` repository...')


if __name__ == '__main__':
    # scan for existing python versions in the system
    python_versions = scan_python_versions()
    # Scan for existing skeletons
    skeletons_list, skeletons = scan_skeletons()
    # parse the arguments
    args, skeleton, skeleton_dir, fullpath = \
        get_arguments(sys.argv, skeletons_list, python_versions)
    # generate the confirmation screen
    print(generate_brief(args))
    # proceed (or not) with the Scaffolding
    proceed = input('\nProceed (yes/no)? ')
    valid = ['yes', 'y', 'no', 'n']

    while True:
        if proceed.lower() in valid:
            if proceed.lower() == 'yes' or proceed.lower() == 'y':
                print('\nScaffolding your',
                      args.appname.upper(), 'application...')

                # create new project's structure and configuration files
                template_ctx = make_structure(
                    args, skeleton, skeleton_dir, fullpath)

                # Add bower dependencies
                if args.bower:
                    bower = args.bower.split(' ')
                    print('Installing bower dependencies...')
                    add_bower(bower, skeleton, fullpath)

                # Add a python virtual environment
                virtualenv = args.virtualenv
                if virtualenv:
                    print('Setting up a Python', args.virtualenv,
                          'virtual environment...')
                    add_virtualenv(fullpath)

                # Add a git repository
                if args.git:
                    print('Initializing a Git repository...')
                    add_git(fullpath)

                print('\nDone. Enjoy it!...\n')
                break
            else:
                print('\nScaffolding aborted by user!\n')
                break
        else:
            print('Please respond with `yes`  or `no` (or `y` or `n`)')
            proceed = input('\nProceed (yes/no)? ')
