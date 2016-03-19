from __future__ import absolute_import
from docutils import nodes
from docutils.parsers.rst import Directive, directives


def align(argument):
    """Conversion function for the "align" option."""
    return directives.choice(argument, ('left', 'center', 'right'))


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


