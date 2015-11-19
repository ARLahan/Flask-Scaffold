# project/config.py
"""Project utilities."""

from . import app
from flask.ext.babelex import format_datetime


class Jinja2Filters(object):
    """Custom template filters."""

    @app.template_filter()
    def datetime_filter(value, format='full'):
        """Convert a datetime to a different format."""
        if format == 'full':
            format = "EEEE, dd MMMM yyyy '@' HH:MM:SS Z"
        elif format == 'medium':
            format = "EE dd.MM.yyyy HH:MM Z"
        elif format == 'short':
            format = "dd.MM.yyyy HH:MM:SS Z"
        return format_datetime(value, format)

    app.jinja_env.filters['datetime'] = datetime_filter
