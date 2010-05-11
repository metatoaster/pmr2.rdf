import unittest
import os
from os.path import dirname, join
from cStringIO import StringIO

import rdflib

from pmr2.rdf.base import RdfXmlObject
from pmr2.rdf.base import RdfXmlMetadata

testroot = dirname(__file__)
input_dir = join(testroot, 'input')
output_dir = join(testroot, 'output')

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.file = RdfXmlObject()

    def tearDown(self):
        pass

    def parse(self, filename):
        fd = open(filename)
        try:
            self.file.parse(fd)
        finally:
            fd.close()

    def test_0000_basic(self):
        self.parse(join(input_dir, 'well-formed-3-node.xml'))
        self.assertEqual(len(self.file.subgraphIds), 3)

    def test_0001_simple(self):
        self.parse(join(input_dir, 'simple.rdf'))
        self.assertEqual(len(self.file.subgraphIds), 1)


class MetadataTestCase(unittest.TestCase):

    def setUp(self):
        self.file = RdfXmlMetadata()

    def tearDown(self):
        pass

    def parse(self, filename):
        fd = open(filename)
        try:
            self.file.parse(fd)
        finally:
            fd.close()

    def test_0000_queryEFNote(self):
        self.parse(join(input_dir, 'well-formed-3-node.xml'))
        answer = {
            u'key1': u'value1',
            u'key2': u'value2',
        }
        # must convert to dictionary for testign because of multiple 
        # results being unordered.
        results = dict(self.file.queryEFNote('ex'))
        self.assertEqual(answer, results)

    def test_0100_queryDC(self):
        self.parse(join(input_dir, 'well-formed-3-node.xml'))
        answer = [(
            ('dc:title', u'Test XML 3 node'),
            ('dc:creator', u'Tommy'), 
            ('dc:description', u'A test RDF/XML document'),
        )]
        # single result set, query ordered.
        results = self.file.queryDC('')
        self.assertEqual(answer, results)

    def test_0101_queryDC_partial(self):
        self.parse(join(input_dir, 'partial_dc.rdf'))
        answer = [(
            ('dc:title', u'Test RDF File'),
            ('dc:creator', u'Example'), 
            ('dc:description', None),
        )]
        # single result set, query ordered.
        results = self.file.queryDC('')
        self.assertEqual(answer, results)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTestCase))
    suite.addTest(unittest.makeSuite(MetadataTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()

