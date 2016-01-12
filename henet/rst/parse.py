import os
import patch

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

    def visit_title(self, node):
        self.article['title'] = node.astext()
        self.article['title_source'] = node.realsource
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
                metadata[name] = value
            else:
                metadata[info.tagname.lower()] = info.astext()
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
    pub.process_programmatic_settings(None, None, None)
    pub.publish()
    return pub.writer.visitor.article


if __name__ == '__main__':

    for file in os.listdir('samples'):
        if not file.endswith('rst') or file.startswith('res-'):
            continue

        filename = os.path.join('samples', file)
        dest = os.path.join('samples', 'res-' + file)
        article = parse_article(filename, dest)
        res = article.render()

        with open(filename) as source:
            with open(dest) as destination:
                source = source.read().strip()
                destination = destination.read().strip()
                source = source.expandtabs(tabsize=4)

                if source != destination:
                    lev_ = distance(source, destination)
                    jaro_ = jaro(source, destination)

                    if lev_ > 10 and jaro_ < 0.85:
                        print('Warning. The file %s was heavily modified' % filename)
                        print('size: %d' % len(source))
                        print('jaro: %f' % jaro_)
                        print('lev: %s' % lev_)
