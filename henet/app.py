# encoding: utf-8
import signal
import sys
import os
from functools import partial
from logging.config import fileConfig

import bottle
from bottle import route, run, view, app as app_stack
from bottle import static_file
import konfig
import multiprocessing_logging

from henet.events import subscribe, ALL_EVENTS, event2str
from henet.workers import MemoryWorkers
from henet.util import send_email
from bottle_utils.i18n import I18NPlugin


HERE = os.path.dirname(__file__)
TEMPLATES = os.path.join(HERE, 'templates')
bottle.TEMPLATE_PATH.append(TEMPLATES)

RESOURCES_PATH = os.path.join(HERE, 'resources')
LOCALES_PATH = os.path.join(HERE, 'locales')
DEFAULT_DEBUG = True
DEFAULT_PORT = 8080
DEFAULT_HOST = 'localhost'
DEFAULT_CONFIG = os.path.join(HERE, '..', 'config.ini')


@route("/resources/<filepath:path>")
def serve_static(filepath):
    return static_file(filepath, root=RESOURCES_PATH)


_alerts = []


def add_alert(event, **data):
    # per-thread ? per-user ?
    _alerts.append(event2str(event))


def get_alerts():
    while True:
        try:
            yield _alerts.pop()
        except IndexError:
            break


def main():
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = DEFAULT_CONFIG

    fileConfig(config_file)
    multiprocessing_logging.install_mp_handler()

    config = konfig.Config(config_file)
    bottle.debug(config['henet'].get('debug', DEFAULT_DEBUG))
    app = bottle.app()

    # bottle config used by bottle-utils
    csrf_config = dict([('csrf.%s' % key, val) for key, val in
                        config.items('csrf')])
    app.config.update(csrf_config)

    # setting up languages
    default_locale = config['henet'].get('default_locale', 'fr_FR')
    langs = [[p.strip() for p in lang.split(',')] for lang
             in config['henet'].get('langs', ['fr_FR'])]

    app = I18NPlugin(app, langs=langs, default_locale=default_locale,
                     locale_dir=LOCALES_PATH)

    cats = []

    config_cats = config['henet']['categories']
    if not isinstance(config_cats, list):
        config_cats = [config_cats]

    for cat in config_cats:
        values = dict(config[cat].items())
        # defaults
        if 'can_create' not in values:
            values['can_create'] = True
        cats.append((cat, values))

    pages = []

    config_pages = config['henet']['pages']
    if not isinstance(config_pages, list):
        config_pages = [config_pages]

    for page in config_pages:
        values = dict(config[page].items())
        # defaults
        if 'can_create' not in values:
            values['can_create'] = True
        pages.append((page, values))

    app_stack.vars = app.vars = {'pages': pages,
                                 'categories': cats,
                                 'get_alerts': get_alerts,
                                 'site_url': config['henet']['site_url'],
                                 'langs': langs}

    app_stack.view = partial(view, **app.vars)
    app_stack._config = app._config = config
    app_stack.workers = app.workers = MemoryWorkers()

    smtp_config = dict(config.items('smtp'))

    def _send_email(*args):
        args = list(args) + [smtp_config]
        app.workers.apply_async('send-email', send_email, args)

    app_stack.send_email = app.send_email = _send_email

    from henet import views  # NOQA

    def _close_workers(*args):
        app.workers.close()
        sys.exit(0)

    subscribe(ALL_EVENTS, add_alert)
    signal.signal(signal.SIGINT, _close_workers)

    run(app=app,
        host=config['henet'].get('host', DEFAULT_HOST),
        port=config['henet'].get('port', DEFAULT_PORT),
        server='waitress')


if __name__ == '__main__':
    main()
