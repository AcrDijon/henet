from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import Directive, directives


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


def key(argument):
    return argument


class OpenRunner(Directive):

    html = ('<script type="text/javascript" src="http://www.openrunner.com/orservice/inorser-script.php?'
            'key=%(key)s&amp;ser=S08&amp;id=%(run_id)s&amp;w=%(width)s&amp;'
            'h=%(height)s&amp;k=5&amp;m=0&amp;ts=%(timestamp)s"></script>')
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'key': key,
        'align': align
    }
    default_width = 750
    default_height = 500
    default_key = 'mykey'

    def _get_raw_source(self):
        return '.. openrunner:: %s\n' % self.arguments[0]

    def run(self):
        self.options['run_id'] = directives.uri(self.arguments[0])
        if not self.options.get('key'):
            self.options['key'] = self.default_key
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        if not self.options.get('height'):
            self.options['height'] = self.default_height
        if not self.options.get('align'):
            self.options['align'] = 'left'
        self.options['timestamp'] = '1459857519'

        node = nodes.raw('', self.html % self.options, format='html')
        node.rawsource = self._get_raw_source()
        return [node]


class IframeVideo(Directive):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'height': directives.nonnegative_int,
        'width': directives.nonnegative_int,
        'align': align,
    }
    default_width = 500
    default_height = 281

    def _get_raw_source(self):
        raise NotImplementedError()

    def run(self):
        self.options['video_id'] = directives.uri(self.arguments[0])
        if not self.options.get('width'):
            self.options['width'] = self.default_width
        if not self.options.get('height'):
            self.options['height'] = self.default_height
        if not self.options.get('align'):
            self.options['align'] = 'left'

        node = nodes.raw('', self.html % self.options, format='html')
        node.rawsource = self._get_raw_source()
        return [node]


class Youtube(IframeVideo):
    html = '<iframe src="http://www.youtube.com/embed/%(video_id)s" \
    width="%(width)u" height="%(height)u" frameborder="0" \
    webkitAllowFullScreen mozallowfullscreen allowfullscreen \
    class="youtube align-%(align)s"></iframe>'

    def _get_raw_source(self):
        return '.. youtube:: %s\n' % self.arguments[0]


class Vimeo(IframeVideo):
    html = '<iframe src="http://player.vimeo.com/video/%(video_id)s" \
    width="%(width)u" height="%(height)u" frameborder="0" \
    webkitAllowFullScreen mozallowfullscreen allowFullScreen \
    class="youtube align-%(align)s"></iframe>'

    def _get_raw_source(self):
        return '.. vimeo:: %s\n' % self.arguments[0]



directives.register_directive('youtube', Youtube)
directives.register_directive('vimeo', Vimeo)
directives.register_directive('openrunner', OpenRunner)
