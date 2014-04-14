import igraph as G
#import epanet2.pyepanet2 as PE
import pyepanet2 as PE


def getGraph(epa):
        edges = epa.linkNodes
        edgeLengths = epa.linkLengths
        edgeRoughness = epa.linkRoughness
        g = G.Graph(directed=True)
        g.add_vertices(len(epa.nodeIds))
        g.vs['name']=map(str,epa.nodeIds)
        g.vs["shape"] = ["rectangle" if t == "reservoir" or t == "tank" else "circle" for t in epa.nodeTypes.itervalues()]
        g.vs['type']=[epa.nodeTypes[int(n)] for n in g.vs['name']]
        g.vs['baseDemand']=[epa.nodeBaseDemand[int(n)] for n in g.vs['name']]
        g.vs['elev']=[epa.nodeElev[int(n)] for n in g.vs['name']]
        g.vs['head']=[epa.nodeHead[int(n)] for n in g.vs['name']]
        for (id,(u,v)) in edges.iteritems():
                g.add_edge(str(u),str(v),length=edgeLengths[id],name=str(id),roughness=edgeRoughness[id])
        g.es['type']=[epa.linkTypes[int(n)] for n in g.es['name']]

        #g.mylayout = g.layout('kk')

        return g
