

# import
import os
import time
import json
import logging
import core as XPDC
from xConfig import assetConfig
reload(XPDC)
reload(assetConfig)

# setup
logger = logging.getLogger(__name__)


class Asset(object):


    def __init__(self, name, assetType=None):

        # fail instancing if no type
        if not assetType:
            raise Exception('This class should never be instanced by itself!')

        # add variables
        self.assetName = name
        self.assetType = assetType
        self.config = assetConfig.DEFAULT

        # initialize 
        self.__getProjectBlock()
        self.__getPaths()


    def __getProjectBlock(self):
        '''
        Get active project block. If none, fail
        '''

        self.project, self.block = XPDC.getProjectBlock()

        if not self.project:
            raise Exception('No project set')

        if not self.block:
            raise Exception('No block set')

        self.blockObj = XPDC.Block()


    def __getPaths(self):
        '''
        Construct the paths for the asset
        '''

        self.blockPath = self.blockObj.getBlockPath()
        if self.assetType:
            self.assetBasePath = os.path.join(self.blockPath, self.assetType)
            self.assetPath = os.path.join(self.assetBasePath, self.assetName)


    def __blockHasAssetType(self):
        return os.path.isdir(self.assetBasePath)


    def __validateAssetType(self):
        if not self.__blockHasAssetType():
            os.mkdir(self.assetBasePath)
            logger.info('created asset type path - {}'.format(self.assetBasePath))


    def __blockHasAsset(self):
        return os.path.isdir(self.assetPath)


    def _validateAsset(self):
        self.__validateAssetType()
        if not self.__blockHasAsset():
            os.mkdir(self.assetPath)
            logger.info('created asset path - {}'.format(self.assetPath))


    def getName(self):
        return self.assetName


    def getType(self):
        return self.assetType


    def getVersionNumbers(self):
        if not self.__blockHasAssetType():
            return []
        if not self.__blockHasAsset():
            return []
        return os.listdir(self.assetPath)


    def getLatestVersionNumber(self):
        if not self.getVersionNumbers():
            return None
        return self.getVersionNumbers()[-1]


    def hasVersions(self):
        return bool(self.getVersionNumbers())


    def _getNewVersionNumber(self):
        if not self.hasVersions():
            return 1
        return int(self.getLatestVersionNumber()) + 1



class AssetVersion(object):

    def __init__(self, asset, version, create=False):
        self.asset = asset
        self.version = version
        self.versionPath = os.path.join(self.asset.assetPath, str(self.version))
        self.sourcePath = os.path.join(self.versionPath, 'source')
        self.sourceFile = os.path.join(self.sourcePath, assetConfig.SOURCEFILENAME)
        self.sourceName = assetConfig.SOURCEFILENAME

        if create:
            self.__validateVersion()
            self.__validateSource()
            self.__validateDefaultRepsLods()
            self.__constructBaseMetaData()
        else:
            if not self.__blockHasVersion():
                raise Exception('Version {} is not valid'.format(self.version))

    def __constructBaseMetaData(self):
        self.metadata = {}
        self.metadata['user'] = os.getenv('USERNAME')
        self.metadata['timecreate'] = time.time()
        self.metadata['timefinalize'] = None


    def __blockHasVersion(self):
        return os.path.isdir(self.versionPath)


    def __validateVersion(self):
        if not self.__blockHasVersion():
            os.mkdir(self.versionPath)
            logger.info('created asset version - {}'.format(self.versionPath))


    def __validateSource(self):
        if not os.path.isdir(self.sourcePath):
            os.mkdir(self.sourcePath)


    def _getDefaultReps(self):
        return self.asset.config.get('reps')


    def _getDefaultLods(self):
        return self.asset.config.get('lods')


    def __validateDefaultRepsLods(self):
        for rep in self._getDefaultReps():
            for lod in self._getDefaultLods():
                self.__validateRepLod(rep, lod)


    def __validateRepLod(self, rep, lod):
        # lod
        lodPath = os.path.join(self.versionPath, lod)
        if not os.path.isdir(lodPath):
            os.mkdir(lodPath)
        # rep       
        repPath = os.path.join(lodPath, rep)
        if not os.path.isdir(repPath):
            os.mkdir(repPath)


    def getMetaDataPath(self):
        metaDataPath = os.path.join(self.versionPath, 'meta.data')
        return metaDataPath


    def _writeMetaData(self):
        self.metadata['timefinalize'] = time.time()
        with open(self.getMetaDataPath(), 'w') as outFile:
            json.dump(self.metadata, outFile, indent=4)


    def addRepLod(self, rep, lod):
        repLodPath = os.path.join(self.versionPath, rep, lod)
        if os.path.isdir(repLodPath):
            raise Exception('You are trying to create a rep lod thats already there!')
        self.__validateRepLod(rep, lod)


    def getReps(self):
        return os.listdir(self.versionPath)


    def getLods(self, rep):
        repPath = os.path.join(self.versionPath, rep)
        return os.listdir(repPath)


    def getVersionString(self):
        return str(self.version)


    def getVersionInt(self):
        return int(self.version)


    def getName(self):
        return self.asset.getName()


    def getType(self):
        return self.asset.getType()


class TimelineAssetVersion(AssetVersion):

    def __init__(self, asset, version, create=False, framestart=1, frameend=1):
        AssetVersion.__init__(self, asset, version, create)

        self.framestart = framestart
        self.frameend = frameend

        if create:
            self.__constructMetaData()

    def __constructMetaData(self):
        self.metadata['fs'] = self.framestart
        self.metadata['fe'] = self.frameend


class Geometry(Asset):

    '''
    Overloads the Asset class with geometry config and type
    '''

    def __init__(self, name):
        Asset.__init__(self, name, 'geometry')

        self.config.update(assetConfig.DEFAULT_GEOMETRY)


class GeometryVersion(TimelineAssetVersion):

    '''
    Overloads the AssetVersion class with geometry metadata
    '''

    def __init__(self, asset, version, create=False, framestart=1, frameend=1):
        TimelineAssetVersion.__init__(self, asset, version, create, framestart, frameend)

        if create:
            self.__constructMetaData()

    def __constructMetaData(self):
        self.metadata['cache'] = None