import logging
import epanet2 as PE

def attrproperty(getter_function):
    class _Object(object):
        def __init__(self, obj):
            self.obj = obj
        def __getitem__(self, attr):
            return getter_function(self.obj, attr)
    return property(_Object)

NODE_TYPES={
        0:"junction",
        1:"reservoir",
        2:"tank"
            }

LINK_TYPES={
        0:"cvipe",
        1:"pipe",
        2:"pump",
        3:"prv",
        4:"psv",
        5:"pbv",
        6:"fcv",
        7:"tcv",
        8:"gpv"
            }

class pyepanet2(object):
        def __init__ (self, inputFile, reportFile, binaryFile):
                self._inputFile = inputFile
                self._reportFile = reportFile
                self._binaryFile = binaryFile
                rc = PE.ENopen(self._inputFile, self._reportFile, self._binaryFile)
                if (rc):
                        logging.warning("ENOpen returned %d" % (rc))

                (status, self._nodeCount) = PE.ENgetcount(PE.EN_NODECOUNT)
                (status, self._tankCount) = PE.ENgetcount(PE.EN_TANKCOUNT)
                (status, self._linkCount) = PE.ENgetcount(PE.EN_LINKCOUNT)
                self._nodeId = {}
                for i in range (1, self._nodeCount+1):
                        (status, self._nodeId[i]) = PE.ENgetnodeid(i)

                self._nodeType = {}
                for i in range (1, self._nodeCount+1):
                        (status, self._nodeId[i]) = PE.ENgetnodeid(i)
                        (status, nodeType) = PE.ENgetnodetype(i)
                        self._nodeType[i] = NODE_TYPES[nodeType]

                self._linkId = {}
                self._linkNodes = {}
                self._linkLength = {}
                self._linkType = {}
                for i in range (1, self._linkCount+1):
                        (status, self._linkId[i]) = PE.ENgetlinkid(i)
                        (status, u,v) = PE.ENgetlinknodes(i)
                        self._linkNodes[i] = (u,v)
                        (status, self._linkLength[i]) = PE.ENgetlinkvalue(i,PE.EN_LENGTH);
                        (status, linkType) = PE.ENgetlinktype(i)
                        self._linkType[i] = LINK_TYPES[linkType]
                        
                self._nodePressure = {}

                logging.debug("Opened %s with %d nodes %d tanks %d links" % (self._inputFile, self._nodeCount, self._tankCount, self._linkCount))

        def __del__(self):
                PE.ENclose()

        def getNodeCount(self):
                return self._nodeCount
        nodeCount = property(getNodeCount)

        def getLinkCount(self):
                return self._linkCount
        linkCount = property(getLinkCount)

        def getTankCount(self):
                return self._tankCount
        tankCount = property(getTankCount)

        @attrproperty
        def linkNodes(self, i):
                (a,u,v) = PE.ENgetlinknodes(i)
                return (u,v)

        @attrproperty
        def linkIsPipe(self,i):
                (a,v) = PE.ENgetlinktype(i)
                return v == PE.EN_PIPE

        @attrproperty
        def linkDiameter(self,i):
                (a,d) = PE.ENgetlinkvalue(i, PE.EN_DIAMETER)
                return d

        @attrproperty
        def linkType(self,i):
                (a,v) = PE.ENgetlinktype(i)
                return v

        @attrproperty
        def linkLength(self,i):
                (a,v) = PE.ENgetlinkvalue(i, PE.EN_LENGTH)
                return v

        @attrproperty
        def linkRoughness(self,i):
                (a,v) = PE.ENgetlinkvalue(i, PE.EN_ROUGHNESS)
                return v

        @attrproperty
        def linkFlow(self,i):
                (a,v) = PE.ENgetlinkvalue(i, PE.EN_FLOW)
                return v

        @attrproperty
        def linkInitStatus(self,i):
                (a,v) = PE.ENgetlinkvalue(i, PE.EN_INITSTATUS)
                return v

        @attrproperty
        def nodeBaseDemand(self,i):
                (a,d) = PE.ENgetnodevalue(i, PE.EN_BASEDEMAND)
                return d

        @attrproperty
        def nodeElev(self,i):
                (a,v) = PE.ENgetnodevalue(i, PE.EN_ELEVATION)
                return v

        @attrproperty
        def nodePattern(self,i):
                (a,v) = PE.ENgetnodevalue(i, PE.EN_PATTERN)
                return v

        @attrproperty
        def nodeHead(self,i):
                (a,v) = PE.ENgetnodevalue(i, PE.EN_HEAD)
                return v

        @attrproperty
        def nodeType(self,i):
                (a,v) = PE.ENgetnodetype(i)
                return v

        def applyDiam(self, diameters):
                for (idx,diam) in zip (range(1,len(diameters) + 1),diameters):
                        #print "setting pipe %d to diam %f" % (idx, diam.diam)
                        PE.ENsetlinkvalue(idx, PE.EN_DIAMETER, diam)

        def openH(self):
                PE.ENopenH()

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
                                logging.warning("Warning ENgetnodevalue returned %d" % (status, ))
                return self._nodePressure[index]

        def getNodeIds(self):
                return self._nodeId
        nodeIds = property(getNodeIds)

        def getNodeTypes(self):
                return self._nodeType
        nodeTypes = property(getNodeTypes)

        @attrproperty
        def nodeId(self, index):
                return self.nodeIds[index]

        def getLinkIds(self):
                return self._linkId
        linkIds = property(getLinkIds)

        @attrproperty
        def linkId(self, index):
                return self.linkIds[index]


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

        def getLinkNodes(self):
                return self._linkNodes
        linkNodes = property(getLinkNodes)

        def getLinkLengths(self):
                return self._linkLength
        linkLengths = property(getLinkLengths)

        def getLinkTypes(self):
                return self._linkType
        linkTypes = property(getLinkTypes)
