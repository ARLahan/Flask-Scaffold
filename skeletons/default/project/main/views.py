# main/views.py
"""Main views."""

from flask import render_template, Blueprint

# Create blueprint
main_blueprint = Blueprint('main', __name__,
                    	   url_prefix='',
                    	   static_folder='static',
                    	   static_url_path='/main/static',
                    	   template_folder='templates')


# main blueprint routes
@main_blueprint.route('/')
def home():
    """Home view."""
    return render_template('home.html')


@main_blueprint.route('/about')
def about():
    """About view."""
    return render_template('about.html')
