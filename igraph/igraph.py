import igraph as G
from pyepanet2.epanet2 import pyepanet2 as PE

class pyepanet2(PE):
        def getGraph(self):
                edges = self._pyEpanet2.linkNodes
                edgeLengths = self._pyEpanet2.linkLengths
                self._graph = G.Graph()
                self._graph.add_vertices(len(self._pyEpanet2.nodeIds))
                self._graph.vs['name']=map(str,self._pyEpanet2.nodeIds)
                self._graph.vs['shape']=map(str,self._pyEpanet2.nodeIds)
                self._graph.vs["shape"] = ["rectangle" if t == "reservoir" or t == "tank" else "circle" for t in self._pyEpanet2.nodeTypes.itervalues()]
                for (id,(u,v)) in edges.iteritems():
                        self._graph.add_edge(str(u),str(v),length=edgeLengths[id],name=id)

                self._graph.mylayout = self._graph.layout('kk')

                return self._graph
