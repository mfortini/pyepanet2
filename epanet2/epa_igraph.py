import igraph as G
#import epanet2.pyepanet2 as PE
import pyepanet2 as PE
import re
from math import sqrt

def _nodedist(u,v):
    return sqrt((u['x']-v['x'])**2+(u['y']-v['y'])**2)


def _getCoordinates(g,epa):
    coordList = []
    with open(epa._inputFile) as f:
        for row in f:
            if re.match('\s*\[COORDINATES\]',row):
                break
        for row in f:
            if re.match('\s*;',row):
                continue
            if re.match('\s*\[',row):
                break
            if row:
                coordList.append(row)

    for coord in coordList:
        try:
            (s_nid,s_x,s_y) = coord.split()
            (x,y) = (float(s_x),float(s_y))
            g.vs.find(s_nid)['x'] = x
            g.vs.find(s_nid)['y'] = y
        except:
            pass

def _getVertices(g,epa):
    coordList = {}
    with open(epa._inputFile) as f:
        for row in f:
            if re.match('\s*\[VERTICES\]',row):
                break
        for row in f:
            if re.match('\s*;',row):
                continue
            if re.match('\s*\[',row):
                break
            if row:
                try:
                    (s_eid,s_x,s_y) = row.split()
                    if not coordList.has_key(s_eid):
                        coordList[s_eid] = []
                    coordList[s_eid].append((float(s_x),float(s_y)))
                except:
                    pass

    for (s_eid,vertices) in coordList.iteritems():
        g.es.find(name=s_eid)['path'] = vertices


# expands the graph by splitting each multilinestring into its components
def expandGraph(g):
    for e in g.es:
        if e['path']:
            if len(e['path'])>2:
                edgevertices=[]
                edgevertices.append(g.vs[e.source]['name'])
                for i in range(1,len(e['path'])-1):
                    vertexname="e"+str(e['name'])+"_"+str(i)
                    (x,y) = e['path'][i]
                    g.add_vertex(name=vertexname,x=x,y=y)
                    edgevertices.append(vertexname)
                edgevertices.append(g.vs[e.target]['name'])


                for i in range(len(e['path']) - 1):
                    u=g.vs.find(edgevertices[i])
                    v=g.vs.find(edgevertices[i+1])
                    g.add_edge(u,v,length=_nodedist(u,v),name=str(e['name']+"_"+str(i)),roughness=e['roughness'],type=e['type'])

                g.delete_edges((e,))

    return g


def getGraph(epa):
        edges = epa.linkNodes
        edgeLengths = epa.linkLengths
        edgeRoughness = epa.linkRoughness
        g = G.Graph(directed=True)
        g.add_vertices(len(epa.nodeIds))
        g.vs['name']=map(str,epa.nodeIds.values())
        g.vs['index']=map(str,epa.nodeIds.keys())
        g.vs["shape"] = ["rectangle" if t == "reservoir" or t == "tank" else "circle" for t in epa.nodeTypes.itervalues()]
        g.vs['type']=[epa.nodeTypes[int(n)] for n in g.vs['index']]
        g.vs['baseDemand']=[epa.nodeBaseDemand[int(n)] for n in g.vs['index']]
        g.vs['elev']=[epa.nodeElev[int(n)] for n in g.vs['index']]
        g.vs['head']=[epa.nodeHead[int(n)] for n in g.vs['index']]
        for (eid,(u,v)) in edges.iteritems():
                g.add_edge(g.vs.find(index=str(u)),g.vs.find(index=str(v)),length=edgeLengths[eid],index=str(eid),roughness=edgeRoughness[eid])
        g.es['type']=[epa.linkTypes[int(n)] for n in g.es['index']]
        g.es['name']=[epa.linkIds[int(n)] for n in g.es['index']]

        _getCoordinates(g,epa)
        _getVertices(g,epa)

        #g.mylayout = g.layout('kk')

        return g
