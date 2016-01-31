# encoding: utf8
import sys
import os
import argparse
from konfig import Config
from pelican.tools.pelican_quickstart import ask


DEFAULTS = {
    'henet': {'host': 'localhost',
              'port': 8080,
              'debug': True,
              'cache_dir': '/tmp/henet',
              'article_url': 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/',
              'pages_url': 'pages/{slug}/',
              'default_locale': 'fr_FR'
              },
    'csrf': {'secret': 'CHANGEME'},
    'smtp': {'host': 'localhost',
             'port': 25,
             'from': 'henet-admin@example.com'}
}


_DEFAULT_PATH = 'config.ini'
_DEFAULT_LANG = 'en_US'
# XXX to translate
_WELCOME = """\
Welcome to Henet.

This script will let you generate a configuration to run Henet against
an existing Pelican blog.
"""


def main():
    parser = argparse.ArgumentParser(
        description="A kickstarter for Henet",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--path', default=_DEFAULT_PATH,
                        help="The path to generate the config file")
    parser.add_argument('-l', '--lang', default=_DEFAULT_LANG,
                        help='Set the default web site language')

    args = parser.parse_args()

    if os.path.exists(args.path):
        print('%r already exists, quitting' % args.path)
        sys.exit(1)

    print(_WELCOME)
    conf = Config(args.path)

    # 'henet' section
    conf.add_section('henet')

    conf['henet']['host'] = ask('Which host do you want to run henet on?',
                                answer=str,
                                default=DEFAULTS['henet']['host'])

    conf['henet']['port'] = ask('Which port do you want to run henet on?',
                                answer=str,
                                default=DEFAULTS['henet']['port'])

    conf['henet']['debug'] = ask('Do you want to run in debug mode?',
                                 answer=bool,
                                 default=DEFAULTS['henet']['debug'])

    while True:
        path = ask('Where is your Pelican content dir?',
                   answer=str)
        # making sure it exists
        if not os.path.exists(path):
            print("Can't find that path, are you sure ?")
        else:
            break

    conf['henet']['pelican_content_path'] = path


