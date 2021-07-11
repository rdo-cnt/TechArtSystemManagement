
from xAssets.reps import utils
reload(utils)





@utils.timeit
def write(fullLodRepPath, sourceFile, framestart, frameend):
	"""Export the file into a directory

	:param fullLodRepPath: Full directory path for LODRep
	:type fullLodRepPath: string
	:param sourceFile: Source file name and extension
	:type sourceFile: string
	:param framestart: First frame
	:type framestart: int
	:param frameend: Last frame
	:type frameend: int
	"""
	utils.openAndPrepSourceFile(sourceFile)
	utils.MC.AbcExport(j='-frameRange {} {} -dataFormat ogawa -root |base -file {}/{}.abc'.format(framestart, frameend, fullLodRepPath, utils.assetConfig.SOURCEFILENAME))

@utils.timeit
def load(assetName, fullLodRepPath):
	"""Load and import a file from a directory

	:param assetName: Asset's name
	:type assetName: string
	:param fullLodRepPath: Full directory path for LODRep
	:type fullLodRepPath: string
	"""
	fullLodRepPath = '{}/{}.abc'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME)
	utils.abcImport(assetName, fullLodRepPath)
