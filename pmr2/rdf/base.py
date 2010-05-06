from cStringIO import StringIO
from lxml import etree

from pmr2.rdf.graph import PMR2Graph

namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
}


class RdfXmlObject(object):
    """
    RDF/XML helper class.
    """

    def __init__(self):
        self._purge()

    def _purge(self):
        self.graph = None
        self.dom = None
        self.subgraphIds = []

    def parse(self, input):
        """\
        Parses a file.  Will overwrite all attributes.
        """

        self._purge()

        if not hasattr(input, 'read'):
            input = StringIO(input)

        self.graph = PMR2Graph()
        self.dom = etree.parse(input)
        self.subgraphIds = []  # maps line number in source to subgraph

        rdfnodes = []
        xpath_expr = [
            './/rdf:RDF',
            '/rdf:RDF',
        ]
        for expr in xpath_expr:
            rdfnodes.extend(self.dom.xpath(expr, namespaces=namespaces))

        for node in rdfnodes:
            s = StringIO(etree.tostring(node))
            s.seek(0)
            subgraph = self.graph.parse(s)
            self.subgraphIds.append((node.sourceline, subgraph.identifier))
