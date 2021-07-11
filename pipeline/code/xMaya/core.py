
import os
import time
import logging
from setup import utils
from xProjectData import core as XPDC
from xAssets import core as XPDA
from xConfig import assetConfig
import maya.cmds as MC
import maya.mel as MM
reload(XPDC)
reload(XPDA)
reload(utils)

# setup
logger = logging.getLogger(__name__)

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        msg = '%r (%r, %r) %2.2f sec' %(method.__name__, args, kw, te-ts)

        print '\n\n%s' %msg
        return result

    return timed
 

def setBlock(block):
    """Create the block directory

    :param block: [description]
    :type block: [type]
    """
    XPDC.setBlock(block)
    refreshHeadsUpDisplay()
    utils.createProjectFolders()


def setProjectBlock(project, block):
    """Create a Project and block directory folder simultaneously

    :param project: Project name
    :type project: string
    :param block: Block name
    :type block: string
    """
    XPDC.setProjectBlock(project, block)
    refreshHeadsUpDisplay()
    utils.createProjectFolders()


def refreshHeadsUpDisplay():
    """Update heads up display with project and block namess
    """
    project, block = XPDC.getProjectBlock()
    projectBlock = '{}/{}'.format(project, block)

    if not MC.headsUpDisplay('projectBlock', q=True, ex=True):
        MC.headsUpDisplay('projectBlock', section=2, block=0, blockSize='medium', label=projectBlock, labelFontSize='large')
    MC.headsUpDisplay('projectBlock', edit=True, section=2, block=0, blockSize='large', label=projectBlock, labelFontSize='large')


def getGeometryObjectForSelection():
    """Set selected xGeometry nodes as a MayaGeometry object

    :return: Maya Geometry object
    :rtype: mayaGeometry
    """
    selection = MC.ls(sl=True, l=True)
    if not len(selection) == 1:
        logger.error('You dont have exactly one object selected')
        return
    dagPath = selection[0]
    if not MC.nodeType(dagPath) == 'xGeometry':
        logger.error('The selected node is not a xGeometry node')
        return
    name = dagPath.split('|')[-1]
    assetObj = MayaGeometry(name, dagPath)
    return assetObj



class MayaGeometry(XPDA.Geometry):
    def __init__(self, name, dagPath=None):
        XPDA.Asset.__init__(self, name, 'geometry')

        self.config.update(assetConfig.DEFAULT_GEOMETRY)
        self.assetDagPath = dagPath


    def __createNewVersion(self, framestart=1, frameend=1):

        if not self.assetDagPath:
            raise Exception('No dagPath set')
        self._validateAsset()
        newVersionNumber = self._getNewVersionNumber()
        versionObj = MayaGeometryVersion(self, newVersionNumber, True, framestart, frameend)
        return versionObj


    def publish(self, framestart=1, frameend=1):

        
        versionObj = self.__createNewVersion(framestart, frameend)
        return versionObj


    def getVersion(self, version):
        versionObj = MayaGeometryVersion(self, version)
        return versionObj



class MayaGeometryVersion(XPDA.GeometryVersion):
    """Overloads the GeometryVersion class, adding methods
    """

    def __init__(self, asset, version, create=False, framestart=1, frameend=1):
        """[summary]

        :param asset: Asset reference
        :type asset: asset
        :param version: Version reference
        :type version: version
        :param create: Should this be created as a folder, defaults to False
        :type create: bool, optional
        :param framestart: First animation frame, defaults to 1
        :type framestart: int, optional
        :param frameend: Last animation frame, defaults to 1
        :type frameend: int, optional
        """
        if create:
            self.__preProcess()

        XPDA.GeometryVersion.__init__(self, asset, version, create, framestart, frameend)

        self.__sourceFile = '{}.mb'.format(self.sourceFile)
        if create:
            self.__prepSaveSourceFileForVersion()
            self.__createReps()
            self.__postProcess()


    def __preProcess(self):
        """Before creating reps, check if the scene is saved

        :raises Exception: File must be saved before publishing
        """
        if MC.file(q=True, modified=True):
            raise Exception('File is not saved. Cannot publish.')
        self.__currentFile = MC.file(q=True, sn=True)


    def __prepSaveSourceFileForVersion(self):
        """Adjust the scene to save only the necessary meshes
        """
        # get node name
        node = self.asset.assetDagPath.split('|')[-1]

        # make sure to set the node to world
        if MC.listRelatives(self.asset.assetDagPath, ap=True):
            MC.parent(self.asset.assetDagPath, w=True)
            self.asset.assetDagPath = '|{}'.format(node)

        # delete everything else
        if self.framestart == self.frameend:
            delNodes = [x for x in MC.ls(dag=True, l=True) if not x.startswith('|{}'.format(node))]
            cams = ['persp', 'top', 'front', 'side']
            for cam in cams:
                delNodes = [x for x in delNodes if not x.startswith('|{}'.format(cam))]
            if delNodes:
                MC.delete(delNodes)

        # make sure transforms are default
        attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        for attr in attrs:
            MC.setAttr('{}.{}'.format(node, attr), 0)
        attrs = ['sx', 'sy', 'sz']
        for attr in attrs:
            MC.setAttr('{}.{}'.format(node, attr), 1)

        # save base
        MC.select('|{}'.format(node))
        MC.file(self.__sourceFile, force=True, options='v=0', typ="mayaBinary", es=True)


    def __createReps(self):
        """Going through the asset's config, go through each lod and rep, then write every file for each repo
        """
        # iterate over all lods and reps and write them out
        for lod in self._getDefaultLods():
            for rep in self._getDefaultReps():
                fullLodRepPath = os.path.join(self.versionPath, lod, rep)
                lodRep = __import__("xAssets.reps.{}.{}".format(lod, rep), fromlist=["xAssets"]) #when moving this to parent object (xasset). To get the lod and reps
                reload(lodRep)
                lodRep.write(fullLodRepPath, self.__sourceFile, self.framestart, self.frameend)

        MC.file(new=True, force=True)


    def __postProcess(self):
        """Write the meta data and open the file after creating it
        """
        self._writeMetaData()
        MC.file(self.__currentFile, force=True, open=True)


    def importAsType(self, lod, rep):
        """Use the lod and reps to import the appropriate

        :param lod: Level of detail name
        :type lod: string
        :param rep: Representation name
        :type rep: string
        """
        # map for different rep types
        repMap = assetConfig.REPMAP
        repPathToken = repMap[rep]

        assetName = self.getName()
        fullLodRepPath = os.path.join(self.versionPath, lod, repPathToken)
        lodRep = __import__("xAssets.reps.{}.{}".format(lod, rep), fromlist=["xAssets"])
        reload(lodRep)
        lodRep.load(assetName, fullLodRepPath)