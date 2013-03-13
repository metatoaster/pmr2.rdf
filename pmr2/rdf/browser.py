from cStringIO import StringIO

import zope.interface
import zope.component

from pmr2.app.workspace.browser.browser import FilePage
from pmr2.app.exposure.browser.browser import ExposureFileRedirect

from pmr2.rdf.base import RdfXmlObject


class RdfPage(FilePage):

    def render(self):
        super(RdfPage, self).update()

        contents = self.data['contents']()
        s = StringIO(contents)
        rdf = RdfXmlObject()
        try:
            rdf.parse(s)
        except:
            pass
        contents = rdf.graph.serialize()

        mimetype = 'application/rdf+xml'
        self.request.response.setHeader('Content-Type', mimetype)
        self.request.response.setHeader('Content-Length', len(contents))
        return contents


class ExposureRdfFileRedirect(ExposureFileRedirect):
    target_view = 'pmr2_rdf'
