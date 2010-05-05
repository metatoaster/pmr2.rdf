import unittest
import os
from os.path import dirname, join
from cStringIO import StringIO

import rdflib

from pmr2.rdf.base import RdfXmlObject

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

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BaseTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()

