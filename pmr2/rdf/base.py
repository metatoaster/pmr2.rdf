from cStringIO import StringIO
from lxml import etree
import rdflib

from pmr2.rdf.graph import PMR2Graph


class RdfXmlObject(object):
    """
    RDF/XML helper class.
    """

    _base_namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    }

    def __init__(self):
        self._purge()

    def _purge(self):
        self.graph = None
        self.dom = None
        self.subgraphIds = []

    @property
    def namespaces(self):
        return self._base_namespaces

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
            rdfnodes.extend(self.dom.xpath(expr, namespaces=self.namespaces))

        for node in rdfnodes:
            s = StringIO(etree.tostring(node))
            s.seek(0)
            subgraph = self.graph.parse(s)
            self.subgraphIds.append((node.sourceline, subgraph.identifier))

    def mergeNs(self, otherNs):
        ns = {}
        ns.update(self.namespaces)
        ns.update(otherNs)
        return ns

    def query(self, q, initBindings={}, otherNs={}):
        ns = self.mergeNs(otherNs)
        return self.graph.query(q, initBindings=initBindings, initNs=ns)

    def queryKeys(self, node, keys, opt_keys=[], otherNs={}):
        """\
        This construct keys/value pair and dynamic simple query.
        """

        # XXX I want to be able to let all values be potentially 
        # optional, but doesn't seem like SPARQL is meant to do that.

        if isinstance(node, basestring):
            node = rdflib.URIRef(node)

        bindings = {
            rdflib.Variable('?node'): node,
        }

        base_q = 'SELECT %s WHERE \n{\n%s}'
        base_stmt = '    ?node %s %s .\n'
        opt_stmt  = '    OPTIONAL { ?node %s %s . }\n'
        frag_key = []
        frag_stmt = []
        for k in keys:
            ns, elem = k.split(':')
            q_key = '?' + elem
            frag_key.append(q_key)
            if k in opt_keys:
                frag_stmt.append(opt_stmt % (k, q_key))
            else:
                frag_stmt.append(base_stmt % (k, q_key))

        q = base_q % (' '.join(frag_key), ''.join(frag_stmt))

        ns = self.mergeNs(otherNs)
        self._lastq = q
        return self.graph.query(q, initBindings=bindings, initNs=ns)


class RdfXmlMetadata(RdfXmlObject):
    """\
    Some sample methods for queries.
    """

    _base_namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'pmr2': 'http://namespace.physiomeproject.org/pmr2#',
        'pmr2note': 'http://namespace.physiomeproject.org/pmr2/note#',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dcterms': 'http://purl.org/dc/terms/',
        'vCard': 'http://www.w3.org/2001/vcard-rdf/3.0#',
    }

    def queryEFNote(self, name):
        """\
        A rough way to get data that may be used to populate an exposure
        file note.
        """

        subject = self.namespaces['pmr2note'] + name
        bindings = {
            rdflib.Variable('?type'): rdflib.URIRef(subject),
        }
        q = """\
        SELECT ?key ?value WHERE {
            ?node pmr2:type ?type .
            ?node pmr2:fields [ ?li ?fnode ] .
            ?fnode pmr2:field [ pmr2:key ?key ] .
            ?fnode pmr2:field [ pmr2:value ?value ] .
        }
        """
        results = self.query(q, bindings, self.namespaces)
        return [(i[0].strip(), i[1].strip()) for i in results]

    def queryDC(self, subject):
        """\
        Returns some Dublin Core information from the target node.
        """

        keys = ['dc:title', 'dc:creator', 'dc:description']
        opt_keys = ['dc:creator', 'dc:description']
        result = self.queryKeys(subject, keys, opt_keys, self.namespaces)
        return [tuple(zip(keys, [j and j.strip() for j in i])) for i in result]
