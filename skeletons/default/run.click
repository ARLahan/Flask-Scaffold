#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Al-Rama Lahan <lahangit@gmail.com>.
"""
Run app choosing which configuration to apply.
Dependencies: `click`.
One can also install `watchdog` as reloader
instead the werkzeug's default which is `stat`,
because `stat` drains laptop's battery.
"""

import os
import click

CONTEXT_SETTINGS = dict(
    default_map={'server': {'port': 5000,
                            'host': 'localhost',
                            'debug': True,
                            'reloading': True,
                            'reloader': 'stat',
                            'environ': 'dev'
                            }
                 }
)


@click.group(context_settings=CONTEXT_SETTINGS)
def run():
    pass


@run.command()
@click.option('--environ', default='pro')
@click.option('--reloader', default='watchdog')
@click.option('--reloading', default=False)
@click.option('--debug', default=False)
@click.option('--port', default=80)
@click.option('--host', default='0.0.0.0')
def server(host, port, debug, reloading, reloader, environ):

    if reloading:
        debug = True

    if environ == "pro":
        os.environ['APP_CONFIG'] = "project.config.ProductionConfig"
        env = "Production configuration"
    elif environ == "test":
        os.environ['APP_CONFIG'] = "project.config.TestingConfig"
        env = "Testing configuration"
    else:
        os.environ['APP_CONFIG'] = "project.config.DevelopmentConfig"
        env = "Development configuration"

    from werkzeug.serving import run_simple
    from project import app

    if environ is "pro":
        click.echo("Serving {app} with {env}".format(app=app, env=env))

    run_simple(host, port, app,
               use_reloader=reloader,
               use_debugger=debug,
               reloader_type=reloader)


if __name__ == '__main__':
    run()
