# main/views.py
"""Main views."""

from flask import render_template, Blueprint

# Create blueprint
main_bp = Blueprint('main', __name__,
                    url_prefix='',
                    static_folder='static',
                    template_folder='templates')


# main blueprint routes
@main_bp.route('/')
def home():
    """Home view."""
    return render_template('main/home.html')


@main_bp.route('/about')
def about():
    """About view."""
    return render_template('main/about.html')
