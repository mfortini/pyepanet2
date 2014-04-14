import igraph as G

def getGraph(self):
        edges = self.linkNodes
        edgeLengths = self.linkLengths
        edgeRoughness = self.linkRoughness
        g = G.Graph(directed=True)
        g.add_vertices(len(self.nodeIds))
        g.vs['name']=map(str,self.nodeIds)
        g.vs["shape"] = ["rectangle" if t == "reservoir" or t == "tank" else "circle" for t in self.nodeTypes.itervalues()]
        g.vs['type']=[self.nodeTypes[int(n)] for n in self._graph.vs['name']]
        g.vs['baseDemand']=[self.nodeBaseDemand[int(n)] for n in self._graph.vs['name']]
        g.vs['elev']=[self.nodeElev[int(n)] for n in self._graph.vs['name']]
        g.vs['head']=[self.nodeHead[int(n)] for n in self._graph.vs['name']]


        edgesToAdd = []
        edgeLengthsToAdd = []
        edgeNamesToAdd = []
        edgeRoughnessesToAdd = []
        for (id,(u,v)) in edges.iteritems():
            edgesToAdd.append((str(u),str(v)))
            edgeLengthsToAdd.append(edgeLengths[id])
            edgeNamesToAdd.append(str(id))
            edgeRoughnessesToAdd.append(edgeRoughness[id])

        g.add_edges(edgesToAdd)

        g.es['length']=edgeLenghtsToAdd
        g.es['name']=edgeNamesToAdd
        g.es['roughness']=edgeRoughnessesToAdd

        #self._graph.mylayout = self._graph.layout('kk')

        return self._graph
