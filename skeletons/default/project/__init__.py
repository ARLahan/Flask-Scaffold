"""Project init."""

import os

from flask import Flask, render_template

app = Flask(__name__)

# Config
# Choose which configuration to use, depending on the value
# assign to the environment variable `APP_CONFIG`:
# --> `DevelopmentConfig`, `TestingConfig` or `ProductionConfig`
app.config.from_object(os.environ['APP_CONFIG'])
app.__str__ = app.config['APP_NAME']  # Define the app name for humans

from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

# Extensions
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Blueprints: import and register
# main blueprint
from .main.views import main_bp
app.register_blueprint(main_bp)
# user blueprint
from .user.views import user_bp
app.register_blueprint(user_bp)

# Login manager
from .user.models import User
login_manager.login_view = "user.login"
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    """Load admin user."""
    return User.query.filter(User.id == int(user_id)).first()


# Error handlers ----------------------------------------------
@app.errorhandler(403)
def forbidden_page(error):
    """Error 403 handler."""
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    """Error 404 handler."""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error_page(error):
    """Error 500 handler."""
    return render_template('errors/500.html'), 500
