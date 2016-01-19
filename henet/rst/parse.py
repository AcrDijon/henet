import os
import patch
import datetime
import re

import dateutil.parser

from docutils.parsers.rst import Parser
from docutils.utils import new_document
from docutils.frontend import OptionParser
from docutils.parsers.rst.states import RSTState, Body, Text
from docutils import nodes
from docutils.nodes import fully_normalize_name as normalize_name
from docutils import writers, statemachine
from docutils.transforms.frontmatter import DocInfo
from docutils.nodes import Element, SkipNode
from docutils import io, core

from Levenshtein import distance, jaro
from pelican.utils import get_date


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


class Article(dict):
    def render(self):
        res = self['title_source'] + '\n\n'
        res += self['metadata_source'] + '\n\n'
        res += self['body']
        if not res.endswith('\n'):
            res += '\n'
        return res


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
        metadata = {}
        for info in node.children:
            if info.tagname == 'field':
                name, body = info.children
                name = name.astext()
                value = body.astext()
                if name in ('date', 'eventdate'):
                    value = get_date(value)
                metadata[name] = value
            else:
                if info.tagname.lower() in ('date', 'eventdate'):
                    value = get_date(info.astext())
                else:
                    value = info.astext()
                metadata[info.tagname.lower()] = value

        self.article['metadata'] = metadata
        self.article['metadata_source'] = node.realsource.strip()
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


def parse_article(filename, destination=None):
    parser = Parser()
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
