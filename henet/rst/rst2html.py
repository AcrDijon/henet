# Adapted from rsted
import os
from os.path import join as J
from StringIO import StringIO
from docutils.core import publish_string, publish_parts


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
    rst_opts['warning_stream'] = StringIO()

    if body_only:
        out = publish_parts(rst, writer_name='html',
                            settings_overrides=rst_opts)['html_body']

        rst_opts['warning_stream'].seek(0)
        warnings = rst_opts['warning_stream'].read()
        return out, warnings

    if opts:
        rst_opts.update(opts)
    rst_opts['template'] = os.path.join(THEMES, 'template.txt')

    stylesheets = ['basic.css']
    if theme:
        stylesheets.append('%s/%s.css' % (theme, theme))
    rst_opts['stylesheet'] = ','.join([J(THEMES, p) for p in stylesheets])

    out = publish_string(rst, writer_name='html', settings_overrides=rst_opts)

    rst_opts['warning_stream'].seek(0)
    warnings = rst_opts['warning_stream'].read()
    return out, warnings
