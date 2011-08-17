try:
    # rdflib 3
    from rdflib.graph import ConjunctiveGraph, Graph
    PMR2Graph = ConjunctiveGraph
    rdflib.plugin.register('sparql', rdflib.query.Processor,
                           'rdfextras.sparql.processor', 'Processor')
    rdflib.plugin.register('sparql', rdflib.query.Result,
                           'rdfextras.sparql.query', 'SPARQLQueryResult')
except ImportError:
    from rdflib.Graph import ConjunctiveGraph, Graph

    class PMR2Graph(ConjunctiveGraph):
        # The parse method of ConjunctiveGraph does not give unique contexts
        # per unique graph parsed.  This brings it more inline with 2.5.x
        # where it does.

        def parse(self, source, publicID=None, format="xml", **args):
            source = self.prepare_input_source(source, publicID)
            id = publicID and \
                self.context_id(source.getPublicId())
            context = Graph(store=self.store, identifier=id)
            context.remove((None, None, None))
            context.parse(source, publicID=publicID, format=format, **args)
            return context

from cStringIO import StringIO
from lxml import etree
import rdflib

namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
}

def parseXML(source, publicID=None, context=None, **args):

    if not hasattr(source, 'read'):
        source = StringIO(source)

    if context is None:
        context = Graph()

    rdfnodes = []
    xpath_expr = [
        './/rdf:RDF',
        '/rdf:RDF',
    ]
    dom = etree.parse(source)
    for expr in xpath_expr:
        rdfnodes.extend(dom.xpath(expr, namespaces=namespaces))
    for node in rdfnodes:
        s = StringIO(etree.tostring(node))
        s.seek(0)
        context.parse(s, publicID=publicID, format='xml', **args)
    return context
