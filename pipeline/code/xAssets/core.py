'''
Module defining the asset class and related classes
'''

# import
import os
import time
import json
import logging
from xProjectData import core as XPDC
from xConfig import assetConfig
reload(XPDC)
reload(assetConfig)

# setup
logger = logging.getLogger(__name__)


class Asset(object):
    """ 
    An asset object. It holds a name, type, config and path to the asset's directory
    """    

    def __init__(self, name, assetType=None):
        """Initialize the asset.

        :param name: Name assigned to the asset
        :type name: string
        :param assetType: Receive the asset type from a child class, defaults to None
        :type assetType: string, optional
        """
        
        
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
        """Get active project block.

        :raises Exception: If an asset doesn't have a project assigned
        :raises Exception: If an asset doesn't have a block assigned
        """

        self.project, self.block = XPDC.getProjectBlock()

        if not self.project:
            raise Exception('No project set')

        if not self.block:
            raise Exception('No block set')

        self.blockObj = XPDC.Block()


    def __getPaths(self):
        """Construct the paths for the asset
        """

        self.blockPath = self.blockObj.getBlockPath()
        if self.assetType:
            self.assetBasePath = os.path.join(self.blockPath, self.assetType)
            self.assetPath = os.path.join(self.assetBasePath, self.assetName)


    def __blockHasAssetType(self):
        """Check if the block has the appropriate asset type folder

        :return: Does the assetType folder exist in the block folder?
        :rtype: bool
        """
        return os.path.isdir(self.assetBasePath)


    def __validateAssetType(self):
        """Create the asset type path if it doesn't exist
        """
        if not self.__blockHasAssetType():
            os.mkdir(self.assetBasePath)
            logger.info('created asset type path - {}'.format(self.assetBasePath))


    def __blockHasAsset(self):
        """Check if the block has an asset folder inside

        :return: Does the asset folder exist in the block folder?
        :rtype: bool
        """
        return os.path.isdir(self.assetPath)


    def _validateAsset(self):
        """Create an asset path if it doesn't exist
        """
        self.__validateAssetType()
        if not self.__blockHasAsset():
            os.mkdir(self.assetPath)
            logger.info('created asset path - {}'.format(self.assetPath))


    def getName(self):
        """Return the asset's name

        :return: Asset Name
        :rtype: string
        """
        return self.assetName


    def getType(self):
        """Return the asset's type

        :return: Asset Type
        :rtype: string
        """
        return self.assetType


    def getVersionNumbers(self):
        """Return the asset's version numbers

        :return: Asset Version number list
        :rtype: List
        """
        if not self.__blockHasAssetType():
            return []
        if not self.__blockHasAsset():
            return []
        return os.listdir(self.assetPath)


    def getLatestVersionNumber(self):
        """Return the asset's latest version

        :return: Return the newest version's number
        :rtype: string
        """
        if not self.getVersionNumbers():
            return None
        return self.getVersionNumbers()[-1]


    def hasVersions(self):
        """Return if the assets have versions

        :return: Does the asset have versions?
        :rtype: bool
        """
        return bool(self.getVersionNumbers())


    def _getNewVersionNumber(self):
        """Returns a brand new number 

        :return: Latest version number + 1
        :rtype: number
        """
        if not self.hasVersions():
            return 1
        return int(self.getLatestVersionNumber()) + 1



class AssetVersion(object):
    """Base actor for an asset's version
    """
    def __init__(self, asset, version, create=False):
        """[summary]

        :param asset: Asset reference
        :type asset: asset
        :param version: Version reference
        :type version: version
        :param create: should a new directory be created?, defaults to False
        :type create: bool, optional
        :raises Exception: The version must exist inside the block folder
        """
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
        """Construct the base meta data JSON information    
        """
        self.metadata = {}
        self.metadata['user'] = os.getenv('USERNAME')
        self.metadata['timecreate'] = time.time()
        self.metadata['timefinalize'] = None


    def __blockHasVersion(self):
        """Check if the block's path has a version folder

        :return: Does the block's path have a version folder?
        :rtype: bool
        """
        return os.path.isdir(self.versionPath)


    def __validateVersion(self):
        """Generate a version directory if it doesn't exist
        """
        if not self.__blockHasVersion():
            os.mkdir(self.versionPath)
            logger.info('created asset version - {}'.format(self.versionPath))


    def __validateSource(self):
        """Generate a source path if it doesn't exist
        """
        if not os.path.isdir(self.sourcePath):
            os.mkdir(self.sourcePath)


    def _getDefaultReps(self):
        """From the config in the Asset, take the reps list

        :return: Representations list
        :rtype: list
        """
        return self.asset.config.get('reps')


    def _getDefaultLods(self):
        """From the config in the Asset, take the lods list

        :return: Level of Details list
        :rtype: list
        """
        return self.asset.config.get('lods')


    def __validateDefaultRepsLods(self):
        """Validate folders for every Level of detail and its inner representations
        """
        for rep in self._getDefaultReps():
            for lod in self._getDefaultLods():
                self.__validateRepLod(rep, lod)


    def __validateRepLod(self, rep, lod):
        """Validate folders for a Level of detail and its specified representation

        :param rep: Representation name
        :type rep: string
        :param lod: Level of Detail name
        :type lod: string
        """
        # lod
        lodPath = os.path.join(self.versionPath, lod)
        if not os.path.isdir(lodPath):
            os.mkdir(lodPath)
        # rep       
        repPath = os.path.join(lodPath, rep)
        if not os.path.isdir(repPath):
            os.mkdir(repPath)


    def getMetaDataPath(self):
        """Return the path for the metadata file

        :return: Metadata file path
        :rtype: string
        """
        metaDataPath = os.path.join(self.versionPath, 'meta.data')
        return metaDataPath


    def _writeMetaData(self):
        """Timestamp and write the metadata file, using this AssetVersion instance's metadata dictionary
        """
        self.metadata['timefinalize'] = time.time()
        with open(self.getMetaDataPath(), 'w') as outFile:
            json.dump(self.metadata, outFile, indent=4)


    def addRepLod(self, rep, lod):
        """[summary]

        :param rep: Representation name
        :type rep: string
        :param lod: Level of detail name
        :type lod: string
        :raises Exception: Rep lod you're trying to generate already exists
        """
        repLodPath = os.path.join(self.versionPath, rep, lod)
        if os.path.isdir(repLodPath):
            raise Exception('You are trying to create a rep lod thats already there!')
        self.__validateRepLod(rep, lod)


    def getReps(self):
        """Get Reps directory list

        :return: Reps directory list
        :rtype: list
        """
        return os.listdir(self.versionPath)


    def getLods(self, rep):
        """Get Reps directory list

        :return: Lods directory list
        :rtype: list
        """
        repPath = os.path.join(self.versionPath, rep)
        return os.listdir(repPath)


    def getVersionString(self):
        """Get the version as a string

        :return: Version number
        :rtype: string
        """
        return str(self.version)


    def getVersionInt(self):
        """Get the version as an integer

        :return: Version number
        :rtype: int
        """
        return int(self.version)


    def getName(self):
        """Returns the asset name

        :return: Asset name
        :rtype: string
        """
        return self.asset.getName()


    def getType(self):
        """Returns the asset type

        :return: Asset type
        :rtype: string
        """
        return self.asset.getType()


class TimelineAssetVersion(AssetVersion):

    """
    Overloads the AssetVersion class with additional frame start and end parameters
    """

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

    """
    Overloads the Asset class with geometry config and type
    """

    def __init__(self, name):
        """Initialize geo

        :param name: Receive name for the asset
        :type name: string
        """
        Asset.__init__(self, name, 'geometry')

        self.config.update(assetConfig.DEFAULT_GEOMETRY)


class GeometryVersion(TimelineAssetVersion):
    
    """ Overloads the AssetVersion class with geometry metadata
    """
    
    def __init__(self, asset, version, create=False, framestart=1, frameend=1):
        """Initialize the geometry

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
        TimelineAssetVersion.__init__(self, asset, version, create, framestart, frameend)

        if create:
            self.__constructMetaData()

    def __constructMetaData(self):
        self.metadata['cache'] = None