import pyepanet2 as PE

def attrproperty(getter_function):
    class _Object(object):
        def __init__(self, obj):
            self.obj = obj
        def __getitem__(self, attr):
            return getter_function(self.obj, attr)
    return property(_Object)

class pyepanet2(object):
        def __init__ (self, inputFile, reportFile, binaryFile):
                self._inputFile = inputFile
                self._reportFile = reportFile
                self._binaryFile = binaryFile
                rc = PE.ENopen(self._inputFile, self._reportFile, self._binaryFile)
                if (rc):
                        print "ENOpen returned %d" % (rc)

                (status, self._nodeCount) = PE.ENgetcount(PE.EN_NODECOUNT)
                (status, self._tankCount) = PE.ENgetcount(PE.EN_TANKCOUNT)
                (status, self._linkCount) = PE.ENgetcount(PE.EN_LINKCOUNT)
                self._nodeId = {}
                for i in range (1, self._nodeCount+1):
                        (status, self._nodeId[i]) = PE.ENgetnodeid(i)

                self._linkId = {}
                for i in range (1, self._linkCount+1):
                        (status, self._linkId[i]) = PE.ENgetlinkid(i)
                        
                self._nodePressure = {}

                print "Opened %s with %d nodes %d tanks %d links" % (self._inputFile, self._nodeCount, self._tankCount, self._linkCount)

        def __del__(self):
                PE.ENclose()

        def getNodeCount(self):
                return self._nodeCount
        nodeCount = property(getNodeCount)

        def getTankCount(self):
                return self._tankCount
        tankCount = property(getTankCount)

        def applyDiam(self, diameters):
                for (idx,diam) in zip (range(1,len(diameters) + 1),diameters):
                        #print "setting pipe %d to diam %f" % (idx, diam.diam)
                        PE.ENsetlinkvalue(idx, PE.EN_DIAMETER, diam)

        def solveH(self):
                self._nodePressure = {}
                #PE.ENopenH()
                PE.ENsolveH()
                #PE.ENcloseH()

        @attrproperty
        def nodePressure(self, index):
                try:
                        return self._nodePressure[index]
                except KeyError:
                        (status, self._nodePressure[index]) = PE.ENgetnodevalue(index, PE.EN_PRESSURE)
                        if status != 0:
                                print "Warning ENgetnodevalue returned %d" % (status, )
                return self._nodePressure[index]

        def getNodeIds(self):
                return self._nodeId
        nodeIds = property(getNodeIds)

        def getLinkIds(self):
                return self._linkId
        linkIds = property(getLinkIds)

        def getNodePressures(self):
                ret = {}
                for i in range(1,self._nodeCount + 1):
                        ret[i] = self.nodePressure[i]
                return ret
        nodePressures = property(getNodePressures)

        def getNodePressuresVector(self):
                ret = [self.nodePressure[i] for i in range(1,self._nodeCount + 1)]
                return ret
        nodePressuresVector = property(getNodePressuresVector)


