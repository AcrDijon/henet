# Adapted from rsted
import os
from os.path import join as J
from docutils.core import publish_string
from bs4 import BeautifulSoup


# see http://docutils.sourceforge.net/docs/user/config.html
default_rst_opts = {
    'no_generator': True,
    'no_source_link': True,
    'tab_width': 4,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'stylesheet_path': None,
    'traceback': True,
    'halt_level': 5,
}

THEMES = os.path.join(os.path.dirname(__file__), 'themes')


# cache + security
def rst2html(rst, theme=None, opts=None, body_only=False):
    rst_opts = default_rst_opts.copy()
    if opts:
        rst_opts.update(opts)
    rst_opts['template'] = os.path.join(THEMES, 'template.txt')

    stylesheets = ['basic.css']
    if theme:
        stylesheets.append('%s/%s.css' % (theme, theme))
    rst_opts['stylesheet'] = ','.join([J(THEMES, p) for p in stylesheets])

    out = publish_string(rst, writer_name='html', settings_overrides=rst_opts)

    # XXX we should create a custom docutils writer to write just the
    # body instead of extracting it from publish_string
    if body_only:
        soup = BeautifulSoup(out, 'html.parser')
        body = soup.body.find('div', {'class':'body'}).contents
        out = ''.join([str(tag) for tag in body])

    return out
