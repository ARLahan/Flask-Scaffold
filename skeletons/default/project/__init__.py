#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Al-Ramaa Lahan <lahangit@gmail.com>.
# NO LICENCE
"""Project init."""

import os

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.babelex import Babel
from flask.ext.bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config for development
app.config.from_object(os.environ['APP_CONFIG'])
app.__str__ = app.config['APP_NAME']  # Define the app name for humans

# Extensions
babel = Babel(app)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


from .user.models import User

# Blueprints: import and register
from .main.views import main_blueprint
from .user.views import user_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)


# Login manager
login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    """Load admin user."""
    return User.query.filter(User.id == int(user_id)).first()


# Error handlers ----------------------------------------------
@app.errorhandler(401)
def forbidden_page(error):
    """Error 401 handler."""
    return render_template('errors/401.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    """Error 404 handler."""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error_page(error):
    """Error 500 handler."""
    return render_template('errors/500.html'), 500


from . import utils

# if in development and debug is true load debug toolbar
if app.config['DEBUG']:
    from flask.ext.debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)
