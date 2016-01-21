from docutils.parsers.rst.states import RSTState, Body, Text
from docutils import nodes
from docutils.nodes import fully_normalize_name as normalize_name
from docutils import statemachine
from docutils.transforms.frontmatter import DocInfo
from docutils.nodes import Element
from docutils.utils.roman import toRoman


def Element__init__(self, rawsource='', *children, **attributes):
    self._old_init(rawsource, *children, **attributes)

Element._old_init = Element.__init__
Element.__init__ = Element__init__


def section(self, title, source, style, lineno, messages):
    if self.check_subsection(source, style, lineno):
        self.new_subsection(title, lineno, messages, source, style)

RSTState.section = section


def new_subsection(self, title, lineno, messages, source, style):
    memo = self.memo
    mylevel = memo.section_level
    memo.section_level += 1
    section_node = nodes.section()
    self.parent += section_node
    textnodes, title_messages = self.inline_text(title, lineno)
    titlenode = nodes.title(title, '', *textnodes)
    titlenode.realsource = source
    titlenode.style = style
    name = normalize_name(titlenode.astext())
    section_node['names'].append(name)
    section_node += titlenode
    section_node += messages
    section_node += title_messages
    self.document.note_implicit_target(section_node, section_node)
    offset = self.state_machine.line_offset + 1
    absoffset = self.state_machine.abs_line_offset() + 1
    newabsoffset = self.nested_parse(
            self.state_machine.input_lines[offset:], input_offset=absoffset,
            node=section_node, match_titles=True)
    self.goto_line(newabsoffset)
    if memo.section_level <= mylevel:
        raise EOFError
    memo.section_level = mylevel


RSTState.new_subsection = new_subsection


def field(self, match):
    name = self.parse_field_marker(match)
    src, srcline = self.state_machine.get_source_and_line()
    lineno = self.state_machine.abs_line_number()
    first = self.state_machine.get_first_known_indented
    indented, indent, line_offset, blank_finish = first(match.end())
    field_node = nodes.field()
    field_node.realsource = match.string
    field_node.source = src
    field_node.line = srcline
    name_nodes, name_messages = self.inline_text(name, lineno)
    field_node += nodes.field_name(name, '', *name_nodes)
    field_body = nodes.field_body('\n'.join(indented), *name_messages)
    field_node += field_body
    if indented:
        self.parse_field_body(indented, line_offset, field_body)
    return field_node, blank_finish


def field_marker(self, match, context, next_state):
    """Field list item."""
    field_list = nodes.field_list()
    self.parent += field_list
    field, blank_finish = self.field(match)
    field_list += field
    offset = self.state_machine.line_offset + 1   # next line
    newline_offset, blank_finish = self.nested_list_parse(
            self.state_machine.input_lines[offset:],
            input_offset=self.state_machine.abs_line_offset() + 1,
            node=field_list, initial_state='FieldList',
            blank_finish=blank_finish)
    self.goto_line(newline_offset)
    if not blank_finish:
        self.parent += self.unindent_warning('Field list')

    raw = self.state_machine.input_lines[offset-1:newline_offset-2].data
    field_list.realsource = '\n'.join(raw)
    return [], next_state, []


def bullet(self, match, context, next_state):
    bulletlist = nodes.bullet_list()
    self.parent += bulletlist
    bulletlist['bullet'] = match.string[0]
    i, blank_finish = self.list_item(match.end())
    bulletlist += i
    offset = self.state_machine.line_offset + 1   # next line
    new_line_offset, blank_finish = self.nested_list_parse(
            self.state_machine.input_lines[offset:],
            input_offset=self.state_machine.abs_line_offset() + 1,
            node=bulletlist, initial_state='BulletList',
            blank_finish=blank_finish)

    raw = []
    indent = '  '

    def _indent(line):
        if line == '':
            return ''
        return indent + line

    prefix = bulletlist['bullet'] + ' '
    for child in bulletlist.children:
        lines = child.rawsource.split('\n')
        lines = [_indent(line) for line in lines]
        raw.append(prefix + '\n'.join(lines).lstrip())

    bulletlist.rawsource = '\n'.join(raw)
    if bulletlist.rawsource.endswith('\n'):
        bulletlist.rawsource = bulletlist.rawsource[:-1]

    self.goto_line(new_line_offset)
    if not blank_finish:
        self.parent += self.unindent_warning('Bullet list')

    return [], next_state, []


def int2enum(value, enum_type):
    if enum_type == 'upperalpha':
        return chr(ord('A') + value - 1)
    elif enum_type == 'loweralpha':
        return chr(ord('a') + value - 1)
    elif enum_type in ('upperroman', 'lowerroman'):
        res = toRoman(value)
        if enum_type == 'upperroman':
            res = res.upper()
        return res
    raise NotImplementedError(enum_type)


def enumerator(self, match, context, next_state):
    format, sequence, text, ordinal = self.parse_enumerator(match)
    if not self.is_enumerated_list_item(ordinal, sequence, format):
        raise statemachine.TransitionCorrection('text')
    enumlist = nodes.enumerated_list()
    self.parent += enumlist
    if sequence == '#':
        enumlist['enumtype'] = 'arabic'
    else:
        enumlist['enumtype'] = sequence
    enumlist['prefix'] = self.enum.formatinfo[format].prefix
    enumlist['suffix'] = self.enum.formatinfo[format].suffix
    if ordinal != 1:
        enumlist['start'] = ordinal
        msg = self.reporter.info(
            'Enumerated list start value not ordinal-1: "%s" (ordinal %s)'
            % (text, ordinal))
        self.parent += msg
    listitem, blank_finish = self.list_item(match.end())
    enumlist += listitem
    offset = self.state_machine.line_offset + 1   # next line
    newline_offset, blank_finish = self.nested_list_parse(
            self.state_machine.input_lines[offset:],
            input_offset=self.state_machine.abs_line_offset() + 1,
            node=enumlist, initial_state='EnumeratedList',
            blank_finish=blank_finish,
            extra_settings={'lastordinal': ordinal,
                            'format': format,
                            'auto': sequence == '#'})

    raw = []
    indent = '  '

    def _indent(line):
        if line == '':
            return ''
        return indent + line

    index = 1

    for child in enumlist.children:
        if enumlist['enumtype'] == 'arabic':
            prefix = '# '
        else:
            prefix = '%s. ' % int2enum(index, enumlist['enumtype'])
            index += 1
        lines = child.rawsource.split('\n')
        lines = [_indent(line) for line in lines]
        raw.append(prefix + '\n'.join(lines).lstrip())

    enumlist.rawsource = '\n'.join(raw)
    if enumlist.rawsource.endswith('\n'):
        enumlist.rawsource = enumlist.rawsource[:-1]

    self.goto_line(newline_offset)
    if not blank_finish:
        self.parent += self.unindent_warning('Enumerated list')
    return [], next_state, []


def line_block(self, match, context, next_state):
    """First line of a line block."""
    block = nodes.line_block()
    self.parent += block
    lineno = self.state_machine.abs_line_number()
    line, messages, blank_finish = self.line_block_line(match, lineno)
    block += line
    self.parent += messages
    if not blank_finish:
        offset = self.state_machine.line_offset + 1   # next line
        new_line_offset, blank_finish = self.nested_list_parse(
                self.state_machine.input_lines[offset:],
                input_offset=self.state_machine.abs_line_offset() + 1,
                node=block, initial_state='LineBlock',
                blank_finish=0)
        self.goto_line(new_line_offset)
    if not blank_finish:
        self.parent += self.reporter.warning(
            'Line block ends without a blank line.',
            line=lineno+1)
    if len(block):
        if block[0].indent is None:
            block[0].indent = 0
        self.nest_line_block_lines(block)

    raw = '\n'.join(['| %s' % child.rawsource for child in block.children])
    block.rawsource = raw
    return [], next_state, []


def block_quote(self, indented, line_offset):
    elements = []

    while indented:
        (blockquote_lines,
            attribution_lines,
            attribution_offset,
            indented,
            new_line_offset) = self.split_attribution(indented, line_offset)

        blockquote = nodes.block_quote()
        blockquote.rawsource = '    ' + '\n'.join(blockquote_lines.data)
        self.nested_parse(blockquote_lines, line_offset, blockquote)
        elements.append(blockquote)
        if attribution_lines:
            attribution, messages = self.parse_attribution(
                attribution_lines, attribution_offset)
            blockquote += attribution
            elements += messages
        line_offset = new_line_offset
        while indented and not indented[0]:
            indented = indented[1:]
            line_offset += 1

    return elements


Body.enumerator = enumerator
Body.bullet = bullet
Body.field = field
Body.field_marker = field_marker
Body.line_block = line_block
Body.block_quote = block_quote


def indent(self, match, context, next_state):
    definitionlist = nodes.definition_list()
    definitionlistitem, blank_finish = self.definition_list_item(context)
    definitionlist += definitionlistitem
    self.parent += definitionlist
    offset = self.state_machine.line_offset + 1   # next line
    newline_offset, blank_finish = self.nested_list_parse(
            self.state_machine.input_lines[offset:],
            input_offset=self.state_machine.abs_line_offset() + 1,
            node=definitionlist, initial_state='DefinitionList',
            blank_finish=blank_finish, blank_finish_state='Definition')

    raw = []
    indent = '  '

    def _indent(line):
        if line == '':
            return ''
        return indent + line

    prefix = '  '

    for child in definitionlist.children:
        line = child.rawsource.split('\n')
        raw.append(line[0])
        for definition in line[1:]:
            if definition == '':
                raw.append('')
            else:
                raw.append(prefix + definition)
        raw.append('')

    definitionlist.rawsource = '\n'.join(raw).strip()
    self.goto_line(newline_offset)
    if not blank_finish:
        self.parent += self.unindent_warning('Definition list')
    return [], 'Body', []


Text.indent = indent


def apply(self):
    if not getattr(self.document.settings, 'docinfo_xform', 1):
        return
    document = self.document
    index = document.first_child_not_matching_class(
            nodes.PreBibliographic)
    if index is None:
        return
    candidate = document[index]
    if isinstance(candidate, nodes.field_list):
        biblioindex = document.first_child_not_matching_class(
                (nodes.Titular, nodes.Decorative))
        nodelist = self.extract_bibliographic(candidate)
        nodelist[0].realsource = candidate.realsource
        del document[index]         # untransformed field list (candidate)
        document[biblioindex:biblioindex] = nodelist


DocInfo.apply = apply
