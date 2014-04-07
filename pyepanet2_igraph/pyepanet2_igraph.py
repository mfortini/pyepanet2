import igraph as G
from pyepanet2.epanet2 import pyepanet2 as PE


class pyepanet2(PE):
        def getGraph(self):
                edges = self.linkNodes
                edgeLengths = self.linkLengths
                edgeRoughness = self.linkRoughness
                self._graph = G.Graph(directed=True)
                self._graph.add_vertices(len(self.nodeIds))
                self._graph.vs['name']=map(str,self.nodeIds)
                self._graph.vs["shape"] = ["rectangle" if t == "reservoir" or t == "tank" else "circle" for t in self.nodeTypes.itervalues()]
                self._graph.vs['type']=[self.nodeTypes[int(n)] for n in self._graph.vs['name']]
                self._graph.vs['baseDemand']=[self.nodeBaseDemand[int(n)] for n in self._graph.vs['name']]
                self._graph.vs['elev']=[self.nodeElev[int(n)] for n in self._graph.vs['name']]
                self._graph.vs['head']=[self.nodeHead[int(n)] for n in self._graph.vs['name']]
                for (id,(u,v)) in edges.iteritems():
                        self._graph.add_edge(str(u),str(v),length=edgeLengths[id],name=str(id),roughness=edgeRoughness[id])

                self._graph.mylayout = self._graph.layout('kk')

                return self._graph
