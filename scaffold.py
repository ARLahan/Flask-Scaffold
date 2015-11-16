#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (2015) Al-Rama Lahan <lahangit@gmail.com>.
"""
Create a new project from a given scaffolding a project skeleton.

Multi-skeleton scaffolder. You just need to put your
application skeletons in the skeleteons directory,
edit this file and add new app skeleton to the skeletons
dictionary, run `scaffold.py` naming your new project and
given its installation location, and you are ready to go.
"""

import sys
import os
import argparse
import jinja2
import codecs
import subprocess
import shutil
import platform

if sys.version_info < (3, 0):
    from shutilwhich import which
    input = raw_input
else:
    from shutil import which


# Globals #
cwd = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))
# Defining the app skeletons
skeletons = {
    # Directory name where are the app skeletons
    'basedir': 'skeletons',
    'skeletons': {
        # skel name | skel sirectory | skeleton name
        'default': {'dir': 'default', 'name': 'project'},
        'src': {'dir': 'src', 'name': 'src'},
    }
}

# Jinja2 environment and location for the templates for scaffolding
template_loader = jinja2.FileSystemLoader(
    searchpath=os.path.join(script_dir, 'templates'))
template_env = jinja2.Environment(loader=template_loader)


def get_arguments(argv):
    """Parsing the received arguments from command line.

    The manadtory argument to pass is the new application name,
    although the path for its installation also should be given or
    the new application will be installed in the current working
    directory in a new directory named with the application name.
    """
    parser = argparse.ArgumentParser(description='Scaffold a Flask Skeleton.')
    parser.add_argument('appname',
                        help='The application name.')
    parser.add_argument('-p', '--path',
                        help='The path where the application \
                              will be located. If none, it will \
                              be installed in the current directory.')
    parser.add_argument('-s', '--skeleton',
                        help='The skeleton to use. \
                        If none, it will choose the default skeleton.')
    parser.add_argument('-b', '--bower',
                        help='Install dependencies via bower. \
                        e.g. syntax: `-b "jquery bootstrap"`')
    parser.add_argument('-v', '--virtualenv', action='store_true',
                        help='Install a virtual environment \
                        based on the current Python version.')
    parser.add_argument('-g', '--git', action='store_true',
                        help='Create a git repository for the application')
    args = parser.parse_args()

    # Variables #
    fullpath = os.path.join(
        args.path, args.appname) \
        if args.path else os.path.join(cwd, args.appname)
    skeleton = skeletons['skeletons'][args.skeleton] \
        if args.skeleton else skeletons['skeletons']['default']
    skeleton_dir = os.path.join(
        cwd, skeletons['basedir'], skeleton['dir'])

    return args, skeleton, skeleton_dir, fullpath


def generate_brief(args):
    """Context dictionary to pass to the scaffold template."""
    template_ctx = {
        'pyversion': platform.python_version(),
        'appname': args.appname,
        'bower': args.bower,
        'virtualenv': args.virtualenv,
        'skeleton': args.skeleton if args.skeleton else 'default',
        'path': args.path if args.path else os.path.join(cwd, args.appname),
        'git': args.git
    }
    template = template_env.get_template('brief.html')
    return template.render(template_ctx)


def make_structure(args, skeleton, skeleton_dir, fullpath):
    """Process the arguments and scaffold the new application."""
    # Copy files and folders
    print('Copying files and folders...')
    shutil.copytree(os.path.join(script_dir, skeleton_dir), fullpath)
    print('Creating the application configuration...')
    secret_key = codecs.encode(os.urandom(64), 'hex').decode('utf-8')
    template_ctx = {
        'secret_key': secret_key,
        'skeleton': skeleton['name'],
        'app_name': args.appname,
    }
    return template_ctx


def make_config(skeleton, fullpath, template_ctx):
    # Create manage.py
    template = template_env.get_template('manage.py.html')
    with open(os.path.join(fullpath, 'manage.py'), 'w') as fd:
        fd.write(template.render(template_ctx))

    # Create the project config.py files
    template = template_env.get_template('config.py.html')
    with open(os.path.join(
            fullpath, skeleton['name'], 'config.py'), 'w') as fd:
        fd.write(template.render(template_ctx))


def make_tests(skeleton, fullpath, template_ctx):
    # Create tests
    template = template_env.get_template('test_base.py.html')
    with open(os.path.join(
            fullpath, 'tests', 'base.py'), 'w') as fd:
        fd.write(template.render(template_ctx))

    template = template_env.get_template('test_config.py.html')
    with open(os.path.join(
            fullpath, 'tests', 'test_config.py'), 'w') as fd:
        fd.write(template.render(template_ctx))

    template = template_env.get_template('test_user.py.html')
    with open(os.path.join(
            fullpath, 'tests', 'test_user.py'), 'w') as fd:
        fd.write(template.render(template_ctx))


def add_bower(bower, skeleton, fullpath):
    bower_exe = which('bower')
    if bower_exe:
        os.chdir(os.path.join(fullpath, skeleton['name'], 'static'))

        for dependency in bower:
            output, error = subprocess.Popen(
                [bower_exe, 'install', dependency],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
            if error:
                print('An error occurred with Bower!')
                print(error)
    else:
        print('Could not find bower. '
              'Ignoring the request for bower '
              'dependencies installation...')


def add_venv(fullpath):
    """Create a python virtual environment named flask."""
    virtualenv_exe = which('pyvenv')
    if virtualenv_exe:
        output, error = subprocess.Popen(
            [virtualenv_exe, os.path.join(fullpath, 'flask')],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()

        if error:
            with open('virtualenv_error.log', 'w') as fd:
                fd.write(error.decode('utf-8'))
                print('An error occurred with virtualenv!')
                sys.exit(2)

        venv_bin = os.path.join(fullpath, 'flask/bin')
        print('Adding application requirements...')
        output, error = subprocess.Popen(
            [
                os.path.join(venv_bin, 'pip'),
                'install',
                '-r',
                os.path.join(fullpath, 'requirements.txt')
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
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
        output, error = subprocess.Popen(
            ['git', 'init', fullpath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        ).communicate()

        if error:
            with open('git_error.log', 'w') as fd:
                fd.write(error.decode('utf-8'))
                print('Error with git init!')
                sys.exit(2)
        print('Adding a `.gitignore` file...')
        shutil.copyfile(
            os.path.join(script_dir, 'templates', '.gitignore'),
            os.path.join(fullpath, '.gitignore')
        )
    else:
        print('Could not find git. '
              'Ignoring the request for initializing '
              'a `.git` repository...')


if __name__ == '__main__':
    args, skeleton, skeleton_dir, fullpath = get_arguments(sys.argv)

    print(generate_brief(args))

    proceed = input('\nProceed (yes/no)? ')
    valid = ['yes', 'y', 'no', 'n']

    while True:
        if proceed.lower() in valid:
            if proceed.lower() == 'yes' or proceed.lower() == 'y':
                print('\nScaffolding your',
                      args.appname.upper(), 'application...')

                # create the structure of the new project
                template_ctx = make_structure(skeleton, skeleton_dir, fullpath)

                # make config
                make_config(skeleton, fullpath, template_ctx)

                # make tests
                make_tests(skeleton, fullpath, template_ctx)

                # Add bower dependencies
                if args.bower:
                    bower = args.bower.split(' ')
                    print('Installing bower dependencies...')
                    add_bower(bower, skeleton, fullpath)

                # Add a python virtual environment
                virtualenv = args.virtualenv
                if virtualenv:
                    print('Setting up a Python', platform.python_version(),
                          'virtual environment...')
                    add_venv(fullpath)

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
