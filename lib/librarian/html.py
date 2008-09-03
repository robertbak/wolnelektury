# -*- coding: utf-8 -*-
import os
import cStringIO
import re
import copy
import pkgutil

from lxml import etree


ENTITY_SUBSTITUTIONS = [
    (u'---', u'—'),
    (u'--', u'–'),
    (u'...', u'…'),
    (u',,', u'„'),
    (u'"', u'”'),
]


def substitute_entities(context, text):
    """XPath extension function converting all entites in passed text."""
    if isinstance(text, list):
        text = ''.join(text)
    for entity, substitutution in ENTITY_SUBSTITUTIONS:
        text = text.replace(entity, substitutution)
    return text


# Register substitute_entities function with lxml
ns = etree.FunctionNamespace('http://wolnelektury.pl/functions')
ns['substitute_entities'] = substitute_entities


def transform(input_filename, output_filename):
    """Transforms file input_filename in XML to output_filename in XHTML."""
    # Parse XSLT
    style_filename = os.path.join(os.path.dirname(__file__), 'book2html.xslt')
    style = etree.parse(style_filename)

    doc_file = cStringIO.StringIO()
    expr = re.compile(r'/\s', re.MULTILINE | re.UNICODE);

    f = open(input_filename, 'r')
    for line in f:
        line = line.decode('utf-8')
        line = expr.sub(u'<br/>\n', line)
        doc_file.write(line.encode('utf-8'))
    f.close()

    doc_file.seek(0);

    parser = etree.XMLParser(remove_blank_text=True)
    doc = etree.parse(doc_file, parser)

    result = doc.xslt(style)
    result.write(output_filename, xml_declaration=True, pretty_print=True, encoding='utf-8')


class Fragment(object):
    def __init__(self, id, themes):
        super(Fragment, self).__init__()
        self.id = id
        self.themes = themes
        self.events = []

    def append(self, event, element):
        self.events.append((event, element))

    def closed_events(self):
        stack = []
        for event, element in self.events:
            if event == 'start':
                stack.append(('end', element))
            elif event == 'end':
                try:
                    stack.pop()
                except IndexError:
                    print 'CLOSED NON-OPEN TAG:', element

        stack.reverse()
        return self.events + stack

    def to_string(self):
        result = []
        for event, element in self.closed_events():
            if event == 'start':
                result.append(u'<%s %s>' % (element.tag, ' '.join('%s="%s"' % (k, v) for k, v in element.attrib.items())))
                if element.text:
                    result.append(element.text)
            elif event == 'end':
                result.append(u'</%s>' % element.tag)
                if element.tail:
                    result.append(element.tail)
            else:
                result.append(element)

        return ''.join(result)

    def __unicode__(self):
        return self.to_string()


def extract_fragments(input_filename):
    """Extracts theme fragments from input_filename."""
    open_fragments = {}
    closed_fragments = {}

    for event, element in etree.iterparse(input_filename, events=('start', 'end')):
        # Process begin and end elements
        if element.tag == 'span' and element.get('class', '') in ('theme-begin', 'theme-end'):
            if not event == 'end': continue # Process elements only once, on end event

            # Open new fragment
            if element.get('class', '') == 'theme-begin':
                fragment = Fragment(id=element.get('fid'), themes=element.text)

                # Append parents
                if element.getparent().tag != 'body':
                    parents = [element.getparent()]
                    while parents[-1].getparent().tag != 'body':
                        parents.append(parents[-1].getparent())

                    parents.reverse()
                    for parent in parents:
                        fragment.append('start', parent)

                open_fragments[fragment.id] = fragment

            # Close existing fragment
            else:
                try:
                    fragment = open_fragments[element.get('fid')]
                except KeyError:
                    print '%s:closed not open fragment #%s' % (input_filename, element.get('fid'))
                else:
                    closed_fragments[fragment.id] = fragment
                    del open_fragments[fragment.id]

            # Append element tail to lost_text (we don't want to lose any text)
            if element.tail:
                for fragment_id in open_fragments:
                    open_fragments[fragment_id].append('text', element.tail)


        # Process all elements except begin and end
        else:
            # Omit annotation tags
            if len(element.get('name', '')) or element.get('class', '') == 'annotation':
                if event == 'end' and element.tail:
                    for fragment_id in open_fragments:
                        open_fragments[fragment_id].append('text', element.tail)
            else:
                for fragment_id in open_fragments:
                    open_fragments[fragment_id].append(event, copy.copy(element))

    return closed_fragments, open_fragments
