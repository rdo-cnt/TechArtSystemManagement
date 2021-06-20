

import maya.OpenMaya as OM
import maya.OpenMayaMPx as OMMP

kPluginNodeTypeName = 'xGeometry' 
node_id = OM.MTypeId(0x8765)
kTransformMatrixID  = OM.MTypeId(0x87015)

class xGeometry(OMMP.MPxTransform):

    def __init__(self):
        OMMP.MPxTransform.__init__(self)

def creator():
    return OMMP.asMPxPtr(xGeometry())

def initializer():
    nAttr = OM.MFnNumericAttribute()
    nAttr.setKeyable(False)

    xGeometry.xGeoVersion = nAttr.create('version', 'bw', OM.MFnNumericData.kFloat)
    xGeometry.addAttribute(xGeometry.xGeoVersion)

def initializePlugin(mobject):
    mplugin = OMMP.MFnPlugin (mobject, 'BCIT Asset Class', '1.0')
    matrix  = OMMP.MPxTransformationMatrix
    mplugin.registerTransform(kPluginNodeTypeName, node_id, creator, initializer, matrix, kTransformMatrixID)

def uninitializePlugin(mobject):
    mplugin = OMMP.MFnPlugin(mobject)
    mplugin.deregisterNode(node_id)