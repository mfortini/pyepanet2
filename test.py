import pyepanet2 as PE

(status,version) = PE.ENgetversion()
print "EPANET version %d" % (version, )

PE.ENopen("../GHEST/hanoi.inp", "pippo.rpt", "")
(status,nnodes) = PE.ENgetcount(PE.EN_NODECOUNT)
(status,ntanks) = PE.ENgetcount(PE.EN_TANKCOUNT)
(status,nlinks) = PE.ENgetcount(PE.EN_LINKCOUNT)

print "Problem has %d nodes and %d tanks and %d links" % (nnodes, ntanks, nlinks)

for i in range(nnodes):
        print PE.ENgetnodeid(i)
        (status, nodeid) = PE.ENgetnodeid(i)
        print "Node %d has id %s" % (i, nodeid)

