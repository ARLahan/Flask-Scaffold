# project/utils.py
# -*- coding: utf-8 -*-
# Author: Al-Ramaa Lahan <lahangit@gmail.com>.

"""Project utilities."""

from . import app
from flask.ext.babelex import format_datetime


@app.template_filter()
def datetime_filter(value, fmt='full'):
    """Convert a datetime to a different format."""
    if fmt == 'extend':
        fmt = "EEEE, dd MMMM yyyy @ HH:mm:ss"
    elif fmt == 'medium':
        fmt = "EE dd.MM.yyyy HH:mm"
    elif fmt == 'short':
        fmt = "dd.MM.yyyy @ HH:mm"
    return format_datetime(value, fmt)

app.jinja_env.filters['datetime'] = datetime_filter
