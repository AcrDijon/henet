from henet.rst import patch  # NOQA

from docutils.parsers.rst import Parser
from docutils.frontend import OptionParser
from docutils import nodes, writers
from docutils.nodes import SkipNode
from docutils import io, core

from pelican.utils import get_date
from henet.article import Article


class Writer(writers.Writer):
    supported = ('txt')
    config_section = 'rst writer'
    config_section_dependencies = ('writers',)

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = RSTTranslator

    def translate(self):
        self.visitor = self.translator_class(self.document)
        self.document.walkabout(self.visitor)
        self.output = self.visitor.astext()


class ThreadWriter(Writer):
    def __init__(self):
        Writer.__init__(self)
        self.translator_class = RSTThreadTranslator


class RSTTranslator(nodes.NodeVisitor):
    def __init__(self, *args, **kw):
        nodes.NodeVisitor.__init__(self, *args, **kw)
        self.result = []
        self.article = Article()
        self._main_title_visited = False

    def visit_title(self, node):
        if not self._main_title_visited:
            self.article['title'] = node.astext()
            self.article['title_source'] = node.realsource
            self._main_title_visited = True

        self.result.append(node.realsource)
        self.result.append('')
        raise SkipNode()

    def visit_docinfo(self, node):
        for info in node.children:
            if info.tagname == 'field':
                name, body = info.children
                name = name.astext()
                value = body.astext()
                if name in ('date', 'eventdate'):
                    value = get_date(value)
                self.article.set_metadata(name, value)
            else:
                if info.tagname.lower() in ('date', 'eventdate'):
                    value = get_date(info.astext())
                else:
                    value = info.astext()
                self.article.set_metadata(info.tagname.lower(), value)

        self.result.append(node.realsource)
        self.result.append('')
        raise SkipNode()

    def visit_enumerated_list(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def visit_block_quote(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def depart_block_quote(self, node):
        pass

    def visit_line_block(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def depart_line_block(self, node):
        pass

    def visit_line(self, node):
        raise NotImplementedError(node)

    def depart_line(self, node):
        pass

    def visit_Text(self, node):
        self.result.append(node.rawsource)

    def depart_Text(self, node):
        pass

    def visit_substitution_definition(self, node):
        self.result.append(node.rawsource)
        raise SkipNode()

    def depart_substitution_definition(self, node):
        pass

    def visit_target(self, node):
        self.result.append(node.rawsource)
        raise SkipNode()

    def depart_target(self, node):
        pass

    def visit_reference(self, node):
        self.result.append(node.rawsource)
        raise SkipNode()

    def visit_transition(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def depart_transition(self, node):
        pass

    def visit_comment(self, node):
        self.result.append(node.rawsource)
        raise SkipNode()

    def depart_comment(self, node):
        pass

    def visit_paragraph(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def visit_image(self, node):
        self.result.append(node.rawsource)
        raise SkipNode()

    def visit_bullet_list(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def visit_definition_list(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def visit_doctest_block(self, node):
        self.result.append(node.rawsource)
        self.result.append('')
        raise SkipNode()

    def visit_section(self, node):
        pass

    def visit_document(self, node):
        pass

    def depart_document(self, node):
        pass

    def depart_section(self, node):
        pass

    def astext(self):
        self.article['body'] = '\n'.join(self.result[4:])
        res = '\n'.join(self.result)
        if res[-1] != '\n':
            res += '\n'
        return res


class RSTThreadTranslator(RSTTranslator):
    def __init__(self, *args, **kw):
        RSTTranslator.__init__(self, *args, **kw)
        self.comments = []
        self.uuid = None
        self.current_comment_index = 0
        self.current_comment = dict()
        self.next_field_name = None

    def visit_docinfo(self, node):
        for info in node.children:
            if info.tagname == 'field':
                name, body = info.children
                name = name.astext()
                if name != 'uuid':
                    continue
                self.uuid = body.astext()

        raise SkipNode()

    def visit_transition(self, node):
        if self.current_comment_index > 0:
            self.current_comment['text'] = u'\n'.join(self.result)
            self.comments.append(self.current_comment)

        # next comment
        self.result = []
        self.current_comment_index += 1
        self.current_comment = dict()

    depart_document = visit_transition

    def visit_field_list(self, node):
        pass

    def visit_field(self, node):
        pass

    def visit_field_name(self, node):
        self.current_field_name = node.astext()
        raise SkipNode()

    def visit_field_body(self, node):
        if self.current_field_name == 'date':
            value = get_date(node.astext())
        elif self.current_field_name == 'active':
            value = node.astext() == '1'
        else:
            value = node.astext()
        self.current_comment[self.current_field_name] = value
        raise SkipNode()

    def depart_field_list(self, node):
        pass

    def depart_field(self, node):
        pass

    def depart_field_name(self, node):
        pass

    def depart_field_body(self, node):
        pass

    def astext(self):
        return ''   # XXX not needed for now


def parse_article(filename, destination=None):
    settings = OptionParser(components=(Parser,)).get_default_values()
    pub = core.Publisher(None, None, None, settings=settings)
    pub.set_components('standalone', 'restructuredtext', 'html')
    pub.writer = Writer()
    pub.set_source(None, filename)

    if destination is not None:
        pub.set_destination(None, destination)
    else:
        pub.destination_class = io.NullOutput
        pub.set_destination(None, None)

    pub.process_programmatic_settings(None, None, None)
    try:
        pub.publish()
    except SystemExit as e:
        raise Exception(str(e))

    return pub.writer.visitor.article


def parse_thread(filename, destination=None):
    settings = OptionParser(components=(Parser,)).get_default_values()
    pub = core.Publisher(None, None, None, settings=settings)
    pub.set_components('standalone', 'restructuredtext', 'html')
    pub.writer = ThreadWriter()
    pub.set_source(None, filename)

    if destination is not None:
        pub.set_destination(None, destination)
    else:
        pub.destination_class = io.NullOutput
        pub.set_destination(None, None)

    pub.process_programmatic_settings(None, None, None)
    try:
        pub.publish()
    except SystemExit as e:
        raise Exception(str(e))

    return pub.writer.visitor.uuid, pub.writer.visitor.comments
