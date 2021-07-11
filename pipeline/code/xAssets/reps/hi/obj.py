
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
	utils.MC.select('|base')
	utils.MC.file('{}/{}.obj'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME), force=True, options='groups=1;ptgroups=1;materials=0;smoothing=1;normals=1', typ='OBJexport', es=True)

@utils.timeit
def load(assetName, fullLodRepPath,*args):
	"""Load and import a file from a directory

	:param assetName: Asset's name
	:type assetName: string
	:param fullLodRepPath: Full directory path for LODRep
	:type fullLodRepPath: string
	"""

	fullLodRepPath = '{}/{}.obj'.format(fullLodRepPath, utils.assetConfig.SOURCEFILENAME)
	utils.objImport(assetName, fullLodRepPath)
