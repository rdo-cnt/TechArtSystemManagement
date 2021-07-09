
import time
import maya.cmds as MC
from xConfig import assetConfig


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        msg = '%r (%r, %r) %2.2f sec' %(method.__name__, args, kw, te-ts)

        print '\n\n%s' %msg
        return result

    return timed


def openAndPrepSourceFile(sourceFile):

	MC.file(sourceFile, force=True, open=True)
	baseNode = MC.createNode('transform', n='base')
	geoNode = MC.ls(type='xGeometry')[0]
	for child in MC.listRelatives(geoNode, f=True):
	    MC.parent(child, baseNode)
	MC.delete(geoNode)
	MC.select(cl=True)


def prepLow():

	meshes = MC.ls(type='mesh', l=True)
	for mesh in meshes:
		MC.polyReduce(	mesh,
						ver=True,  
		        		trm=0,
				        shp=0.4,
				        keepBorder=True,
				        keepMapBorder=False,
				        keepColorBorder=False,
				        keepFaceGroupBorder=False,
				        keepHardEdge=False,
				        keepCreaseEdge=False,
				        keepBorderWeight=0.5,
				        keepMapBorderWeight=0.5,
				        keepColorBorderWeight=0.5,
				        keepFaceGroupBorderWeight=0.5,
				        keepHardEdgeWeight=0.5,
				        keepCreaseEdgeWeight=1,
				        useVirtualSymmetry=0,
				        symmetryTolerance=0.01,
				        sx=0,
				        sy=1,
				        sz=0,
				        sw=0,
				        preserveTopology=1,
				        keepQuadsWeight=0.4,
				        vertexMapName="",
				        cachingReduce=1,
				        ch=False,
				        p=93,
				        vct=0, 
				        tct=0,
				        replaceOriginal=1)


def abcImport(assetName, fullRepLodPath):
	assetNode = MC.createNode('xGeometry', n=assetName)
	baseNode = '{}|base'.format(assetNode)
	MC.AbcImport(fullRepLodPath, reparent='|{}'.format(assetNode), mode='import')
	for child in MC.listRelatives(baseNode, f=True):
	    MC.parent(child, assetNode)
	MC.delete(baseNode)
	MC.select(assetNode)


def abcGpuImport(assetName, fullRepLodPath):
	assetNode = MC.createNode('xGeometry', n=assetName)
	assetTfNode = MC.createNode('transform', n='{}Gpu'.format(assetName), parent=assetNode)
	assetShapeNode = MC.createNode('gpuCache', n='{}GpuShape'.format(assetName), parent=assetTfNode)
	MC.setAttr('{}.cacheFileName'.format(assetShapeNode), fullRepLodPath, type='string')
	MC.select(assetNode)

def objImport(assetName, fullRepLodPath):
	assetNode = MC.createNode('xGeometry', n=assetName)
	baseNode = '{}|base'.format(assetNode)
	import_nodes = MC.file(fullRepLodPath,i=True,type="OBJ",rpr="OBJ_Import",rnn=True)
	# MC.file(fullRepLodPath, reparent='|{}'.format(assetNode), mode='import')
	for child in MC.listRelatives(import_nodes, f=True):
	    MC.parent(child, assetNode)
	MC.select(assetNode)

