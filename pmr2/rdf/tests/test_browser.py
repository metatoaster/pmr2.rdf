from Zope2.App import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import onsetup, onteardown

from pmr2.app.workspace.content import WorkspaceContainer, Workspace
from pmr2.app.workspace.tests import storage
from pmr2.app.workspace.tests import base

from pmr2.app.exposure.content import ExposureContainer, Exposure, ExposureFile

@onsetup
def setup():
    import pmr2.rdf
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.rdf)
    fiveconfigure.debug_mode = False

@onteardown
def teardown():
    pass

setup()
teardown()

storage.DummyStorageUtility._dummy_storage_data['rdftest'] = [
    {
    'test.rdf': """\
<?xml version="1.0" encoding="utf-8"?>
<ex xmlns="http://example.com/ex/1.0#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

  <node>
    <node>
      <rdf:RDF>
        <rdf:Description rdf:about="#item">
          <dc:creator>Example User</dc:creator>
          <dc:title>Test RDF Document</dc:title>
        </rdf:Description>
      </rdf:RDF>
    </node>
  </node>

  <line>
    <rdf:RDF>
      <rdf:Description rdf:about="#item2">
        <dc:creator>Second User</dc:creator>
        <dc:title>Second Item</dc:title>
      </rdf:Description>
    </rdf:RDF>
  </line>

</ex>
""",

    'brokenxml.rdf': """\
<?xml version="1.0" encoding="utf-8"?>
<ex xmlns="http://example.com/ex/1.0#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

  <node>
    <node>
      <rdf:RDF>
        <rdf:Description rdf:about="#item">
          <dc:creator>Example User</dc:creator>
          <dc:title>Test RDF Document</dc:title>
        </rdf:Description>
      </rdf:RDF>
  </node

</ex>
""",

}]

extracted = """\
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <rdf:Description rdf:about="#item">
    <dc:creator>Example User</dc:creator>
    <dc:title>Test RDF Document</dc:title>
  </rdf:Description>
  <rdf:Description rdf:about="#item2">
    <dc:creator>Second User</dc:creator>
    <dc:title>Second Item</dc:title>
  </rdf:Description>
</rdf:RDF>
"""

empty = """\
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
</rdf:RDF>
"""

class RdfViewDocTestCase(base.WorkspaceDocTestCase):

    def setUp(self):
        super(RdfViewDocTestCase, self).setUp()
        self.portal['workspace'] = WorkspaceContainer()
        w = Workspace('rdftest')
        w.storage = 'dummy_storage' 
        self.portal.workspace['rdftest'] = w

        self.portal['exposure'] = ExposureContainer()
        e = Exposure('rdftest')
        e.workspace = u'/plone/workspace/rdftest'
        e.commit_id = u'0'
        self.portal.exposure['rdftest'] = e
        ef = ExposureFile('test.rdf')
        self.portal.exposure.rdftest['test.rdf'] = ef

    def test_0000_base(self):
        self.testbrowser.open(self.portal.absolute_url() +
            '/workspace/rdftest/pmr2_rdf/0/test.rdf')
        contents = self.testbrowser.contents
        self.assertTrue('<dc:creator>Example User</dc:creator>' in contents)
        self.assertTrue('<dc:title>Test RDF Document</dc:title>' in contents)
        self.assertTrue('<dc:creator>Second User</dc:creator>' in contents)
        self.assertTrue('<dc:title>Second Item</dc:title>' in contents)

        self.assertEqual(self.testbrowser.headers['Content-type'],
            'application/rdf+xml')

    def test_0001_broken(self):
        self.testbrowser.open(self.portal.absolute_url() +
            '/workspace/rdftest/pmr2_rdf/0/brokenxml.rdf')
        contents = self.testbrowser.contents
        self.assertEqual(contents, empty)

    def test_0100_exposure_file_redirect(self):
        self.testbrowser.open(self.portal.absolute_url() +
            '/exposure/rdftest/test.rdf/pmr2_rdf')
        self.assertEqual(self.testbrowser.url,
            'http://nohost/plone/workspace/rdftest/@@pmr2_rdf/0/test.rdf')
