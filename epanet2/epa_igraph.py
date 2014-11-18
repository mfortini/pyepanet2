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
    edges_to_del = []
    for e in g.es:
        if e['path']:
            if len(e['path'])>2:
                u=g.vs[e.source]
                v=g.vs[e.target]

                (x,y) = e['path'][0]
                pathstart = {'x':x,'y':y}
                (x,y) = e['path'][-1]
                pathend = {'x':x,'y':y}

                if (_nodedist(u,pathend) < _nodedist(u,pathstart)):
                    e['path'].reverse()

                edgevertices=[]
                edgevertices.append(u['name'])

                (x,y) = e['path'][0]
                if x != u['x'] or y != u['y']:
                    vertexname="e"+str(e['name'])+"_"+str(0)
                    g.add_vertex(name=vertexname,x=x,y=y)
                    edgevertices.append(vertexname)

                for i in range(1,len(e['path'])-1):
                    vertexname="e"+str(e['name'])+"_"+str(i)
                    (x,y) = e['path'][i]
                    g.add_vertex(name=vertexname,x=x,y=y)
                    edgevertices.append(vertexname)

                (x,y) = e['path'][-1]
                if x != v['x'] or y != v['y']:
                    vertexname="e"+str(e['name'])+"_"+str(len(e['path']))
                    g.add_vertex(name=vertexname,x=x,y=y)
                    edgevertices.append(vertexname)

                edgevertices.append(v['name'])


                for i in range(len(edgevertices) - 1):
                    u=g.vs.find(edgevertices[i])
                    v=g.vs.find(edgevertices[i+1])
                    g.add_edge(u,v,length=_nodedist(u,v),DN=e['DN'],DNmm=e['DN'],name=str(e['name']+"_"+str(i)),roughness=e['roughness'],type=e['type'],pipe_name=e['name'])

                edges_to_del.append(e)

    g.delete_edges(edges_to_del)
    return g

def printINP(g):
    print '[JUNCTIONS]'
    for v in g.vs(type='junction'):
        print '%-16s\t%-16s\t%-16s\t;' % (v['name'],v['elev'],v['baseDemand'])

    print '[RESERVOIRS]'
    for v in g.vs(type='reservoir'):
        print '%-16s\t%-16s\t;' % (v['name'],v['head'])

    print '[TANKS]'
    for v in g.vs(type='tank'):
        print '%-16s\t%-16s\t;' % (v['name'],v['elev'])

    print '[PIPES]'
    for e in g.es:
        print '%-16s\t%-16s\t%-16s\t%-16s\t%-16s\t%-16s\t%-16s\t%-16s\t;' % (e['name'],g.vs[e.source]['name'],g.vs[e.target]['name'],e['length'],e['DN'],e['roughness'],0,e['status'])

def getGraph(epa):
        edges = epa.linkNodes
        edgeLengths = epa.linkLengths
        edgeRoughness = epa.linkRoughness
        edgeDiameter = epa.linkDiameter
        g = G.Graph(directed=False)
        g.add_vertices(len(epa.nodeIds))
        g.vs['name']=map(str,epa.nodeIds.values())
        g.vs['index']=map(str,epa.nodeIds.keys())
        g.vs["shape"] = ["rectangle" if t == "reservoir" or t == "tank" else "circle" for t in epa.nodeTypes.itervalues()]
        g.vs['type']=[epa.nodeTypes[int(n)] for n in g.vs['index']]
        g.vs['baseDemand']=[epa.nodeBaseDemand[int(n)] for n in g.vs['index']]
        g.vs['elev']=[epa.nodeElev[int(n)] for n in g.vs['index']]
        g.vs['head']=[epa.nodeHead[int(n)] for n in g.vs['index']]
        for (eid,(u,v)) in edges.iteritems():
                g.add_edge(g.vs.find(index=str(u)),g.vs.find(index=str(v)),length=edgeLengths[eid],index=str(eid),roughness=edgeRoughness[eid],DN=edgeDiameter[eid]/1000., DNmm = edgeDiameter[eid])
        g.es['type']=[epa.linkTypes[int(n)] for n in g.es['index']]
        g.es['name']=[epa.linkIds[int(n)] for n in g.es['index']]
        g.es['pipe_name']=g.es['name']
        g.es['status']=['closed' if epa.linkInitStatus[int(n)] == 0 else 'open' for n in g.es['index']]

        _getCoordinates(g,epa)
        _getVertices(g,epa)

        #g.mylayout = g.layout('kk')

        return g
