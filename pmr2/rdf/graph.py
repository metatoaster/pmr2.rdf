try:
    from rdflib.graph import ConjunctiveGraph
    PMR2Graph = ConjunctiveGraph
except ImportError:
    from rdflib.Graph import ConjunctiveGraph, Graph

    class PMR2Graph(ConjunctiveGraph):
        # The parse method of ConjunctiveGraph does not give unique contexts
        # per unique graph parsed.  This brings it more inline with 2.5.x
        # where it does.

        def parse(self, source, publicID=None, format="xml", **args):
            source = self.prepare_input_source(source, publicID)
            id = publicID and \
                self.context_id(self.absolutize(source.getPublicId()))
            context = Graph(store=self.store, identifier=id)
            context.remove((None, None, None))
            context.parse(source, publicID=publicID, format=format, **args)
            return context
